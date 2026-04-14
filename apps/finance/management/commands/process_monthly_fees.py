import logging
from datetime import date
from decimal import Decimal, ROUND_UP

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.education.models import GroupStudent
from apps.finance.models import Transaction, TransactionCategory, Account, MonthlyFeeLog
from apps.users.models import User
from apps.organizations.models import Organization

logger = logging.getLogger(__name__)


def calculate_price_with_bonus(base_price, student):
    """
    Kurs narxidan bonusni ayirib, yakuniy narxni qaytaradi.
    Avval foiz bonus, keyin summa bonus chegiriladi.
    """
    final_price = base_price

    if student.bonus_percentage > 0:
        final_price = final_price * (1 - (Decimal(student.bonus_percentage) / Decimal(100)))

    if student.bonus_amount > 0:
        final_price = max(Decimal('0'), final_price - student.bonus_amount)

    return final_price.quantize(Decimal('1'), rounding=ROUND_UP)


class Command(BaseCommand):
    help = "Barcha faol o'quvchilar uchun oydagi kutilgan to'lovni avtomatik hisoblab, balansdan yechadi."

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help="Oy boshida bo'lmasaham (test maqsadida) majburlab ishga tushirish",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        today = date.today()
        billing_month = date(today.year, today.month, 1)
        is_force = options['force']

        if today.day != 1 and not is_force:
            self.stdout.write(self.style.WARNING(
                "Bugun oyning boshi emas. Skript to'xtatildi. (--force qo'shing)"
            ))
            return

        for org in Organization.objects.all():
            self._process_organization(org, billing_month, is_force)

        self.stdout.write(self.style.SUCCESS("Barcha tashkilotlar uchun jarayon yakunlandi."))

    def _process_organization(self, org, billing_month, is_force):
        """Bitta tashkilot uchun oylik to'lovlarni yechish."""

        # 1. Shu oy uchun log
        log, _ = MonthlyFeeLog.objects.get_or_create(
            organization=org,
            billing_month=billing_month,
            defaults={'is_processed': False}
        )

        if log.is_processed and not is_force:
            self.stdout.write(self.style.SUCCESS(
                f"[{org.name}] {billing_month} oyi uchun allaqachon yechildi."
            ))
            return

        # 2. Faol guruh-studentlar
        active_gs = GroupStudent.objects.filter(
            group__organization=org,
            status='active',
            student__role='student'
        ).select_related('group__course', 'student')

        if not active_gs.exists():
            self.stdout.write(self.style.WARNING(f"[{org.name}] Faol o'quvchilar topilmadi."))
            return

        # 3. Kategoriya, Kassa, System user (har bir org uchun 1 marta)
        category, _ = TransactionCategory.objects.get_or_create(
            organization=org,
            name="Kurs to'lovi (Oylik avtomat)",
            defaults={'transaction_type': 'income'}
        )

        virtual_account = Account.objects.filter(organization=org).first()
        if not virtual_account:
            self.stdout.write(self.style.ERROR(f"[{org.name}] Kassa topilmadi. O'tkazib yuborildi."))
            return

        system_user = (
            User.objects.filter(role='super_admin', organization=org).first()
            or User.objects.filter(role='super_admin').first()
        )

        # 4. Har bir guruh-student uchun to'lov
        total_amount = Decimal('0')
        billed_students = set()

        for gs in active_gs:
            student = gs.student
            course = gs.group.course

            base_price = course.price if course.price > 0 else Decimal('0')
            if base_price == 0:
                continue

            # Bonusni chegirib narxni hisoblaymiz
            final_price = calculate_price_with_bonus(base_price, student)
            if final_price <= 0:
                continue

            # Tranzaksiya yaratamiz (monthly_fee - kassaga ta'sir qilmaydi)
            new_trans = Transaction(
                organization=org,
                account=virtual_account,
                category=category,
                student=student,
                amount=final_price,
                transaction_type='monthly_fee',
                status='confirmed',
                created_by=system_user,
                confirmed_by=system_user,
                confirmed_at=timezone.now(),
                description=(
                    f"{gs.group.name} - {billing_month.strftime('%Y-%m')} oyi uchun "
                    f"avtomatik to'lov ({final_price:,.0f} UZS)"
                )
            )
            new_trans.is_auto_billing = True
            new_trans.save()

            total_amount += final_price
            billed_students.add(student.id)

            logger.info(
                f"Student #{student.id} ({student.full_name}): "
                f"-{final_price:,.0f} UZS, Yangi balans: {student.balance}"
            )

        # 5. Log yozamiz
        log.is_processed = True
        log.processed_at = timezone.now()
        log.total_students_billed = len(billed_students)
        log.total_amount_billed = total_amount
        log.save(update_fields=['is_processed', 'processed_at', 'total_students_billed', 'total_amount_billed'])

        self.stdout.write(self.style.SUCCESS(
            f"[{org.name}] {len(billed_students)} ta o'quvchidan "
            f"jami {total_amount:,.0f} UZS yechildi."
        ))
