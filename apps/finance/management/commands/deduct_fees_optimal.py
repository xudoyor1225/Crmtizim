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
    help = "Barcha faol o'quvchilardan joriy oy uchun TO'LIQ OYLIK to'lovni OPTIMAL (bulk) shaklda yechish."

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help="Oy boshida bo'lmasa ham majburlab ishga tushirish (test maqsadida)",
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

        self.stdout.write(self.style.WARNING(f"\n=== OPTIMAL OYLIK TO'LOV YECHISH (BULK) ({billing_month.strftime('%Y-%m')}) ==="))

        for org in Organization.objects.all():
            self._process_organization(org, billing_month, today, is_force)

        self.stdout.write(self.style.SUCCESS("\nBarcha tashkilotlar uchun jarayon yakunlandi."))

    def _process_organization(self, org, billing_month, today, is_force):
        # Tashkilot uchun log olamiz
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

        # Faol o'quvchilarni guruh-student bog'lamasi orqali topamiz
        active_gs = list(GroupStudent.objects.filter(
            group__organization=org,
            status='active',
            student__role='student'
        ).select_related('group__course', 'student'))

        if not active_gs:
            return

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

        transactions_to_create = []
        students_to_update = {}
        total_amount = Decimal('0')
        billed_students = set()

        self.stdout.write(f"\n[{org.name}] hisoblanmoqda...")

        for gs in active_gs:
            student = gs.student
            group = gs.group
            course = group.course

            base_price = course.price if course.price > 0 else Decimal('0')
            if base_price == 0:
                continue

            # Bonusni hisobga olgan holda to'liq narxni hisoblaymiz
            full_price = calculate_price_with_bonus(base_price, student)
            if full_price <= 0:
                continue
                
            amount_to_deduct = full_price

            desc = (
                f"{group.name} - {billing_month.strftime('%Y-%m')} oyi uchun "
                f"avtomatik to'lov ({amount_to_deduct:,.0f} UZS)"
            )

            # Tranzaksiyani tayyorlaymiz lekin bazaga SAQLAMAYMIZ (save() qilinmaydi)
            new_trans = Transaction(
                organization=org,
                account=virtual_account,
                category=category,
                student=student,
                amount=amount_to_deduct,
                transaction_type='monthly_fee',
                status='confirmed',
                created_by=system_user or student,
                confirmed_by=system_user or student,
                confirmed_at=timezone.now(),
                description=desc,
            )
            new_trans.is_auto_billing = True
            
            transactions_to_create.append(new_trans)
            
            # Student oldin ham darsga qatnashayotgan bo'lsa (yana bir xil student bir necha guruhda bo'lishi mumkin)
            if student.id not in students_to_update:
                students_to_update[student.id] = student
                
            # Xotirada student balansidan summani ayiramiz
            students_to_update[student.id].balance -= amount_to_deduct
            
            total_amount += amount_to_deduct
            billed_students.add(student.id)

        # Bulk amalga oshirish: bu signals larni trigger qilmaydi, demak balansni ham ikki martalab manfiy tushirmaydi.
        if transactions_to_create:
            # Barcha tranzaksiyalar bitta so'rovda saqlanadi
            Transaction.objects.bulk_create(transactions_to_create, batch_size=500)
            
            # Xotiradagi (yangilangan balansli) hamma userlarni bitta so'rovda saqlaymiz
            users_list = list(students_to_update.values())
            User.objects.bulk_update(users_list, ['balance'], batch_size=500)

            self.stdout.write(self.style.SUCCESS(
                f"  -> {len(billed_students)} ta o'quvchidan (jami {len(transactions_to_create)} marta) {total_amount:,.0f} UZS bittada yechildi."
            ))
            
            # Log jadvalida ma'lumotlarni yangilab qo'yamiz
            log.is_processed = True
            log.processed_at = timezone.now()
            log.total_students_billed = (log.total_students_billed or 0) + len(billed_students)
            log.total_amount_billed = (log.total_amount_billed or Decimal('0')) + total_amount
            log.save(update_fields=['is_processed', 'processed_at', 'total_students_billed', 'total_amount_billed'])

        else:
            self.stdout.write(self.style.WARNING(f"[{org.name}] Yechish uchun qarzdorliklar topilmadi."))
