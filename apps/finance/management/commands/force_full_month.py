import logging
from datetime import date
from decimal import Decimal, ROUND_UP

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.education.models import GroupStudent
from apps.finance.models import Transaction, TransactionCategory, Account, MonthlyFeeLog
from apps.users.models import User
from apps.organizations.models import Organization
from apps.education.signals import calculate_price_with_bonus

class Command(BaseCommand):
    help = "Barcha faol o'quvchilardan TO'LIQ OYLIK to'lovni aniq yechib olish. Agar oldinroq proporsional yechilgan bo'lsa, yetmagan qismini yechadi."

    @transaction.atomic
    def handle(self, *args, **options):
        today = date.today()
        billing_month = date(today.year, today.month, 1)

        self.stdout.write(self.style.WARNING(f"\n=== TO'LIQ OY UCHUN MAJBURIY YECHISH ({billing_month.strftime('%Y-%m')}) ==="))

        for org in Organization.objects.all():
            self._process_organization(org, billing_month, today)

        self.stdout.write(self.style.SUCCESS("\nBarcha tashkilotlar uchun to'liq oylik yechish yakunlandi."))

    def _process_organization(self, org, billing_month, today):
        """Bitta tashkilot uchun oylik to'lovlarni yetmagan qismini yechish."""

        # Faol guruh-studentlar
        active_gs = GroupStudent.objects.filter(
            group__organization=org,
            status='active',
            student__role='student'
        ).select_related('group__course', 'student')

        if not active_gs.exists():
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

        total_amount = Decimal('0')
        billed_count = 0

        self.stdout.write(f"\n[{org.name}] tekshirilmoqda...")

        for gs in active_gs:
            student = gs.student
            group = gs.group
            course = group.course

            base_price = course.price if course.price > 0 else Decimal('0')
            if base_price == 0:
                continue

            # Bonusni chegirib TO'LIQ oylik narxni hisoblaymiz
            full_price = calculate_price_with_bonus(base_price, student)
            if full_price <= 0:
                continue

            desc_search = f"{group.name} - {billing_month.strftime('%Y-%m')} oyi"
            
            # Shu oyni uchun shu guruhdan jami qancha yechilganini summasini hisoblaymiz
            billed_sum = Transaction.objects.filter(
                student=student,
                organization=org,
                transaction_type='monthly_fee',
                description__contains=desc_search,
                created_at__year=today.year,
                created_at__month=today.month
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

            # Yetisheyotgan qismini hisoblaymiz (masalan proporsional yechilgan bo'lsa)
            remaining_price = full_price - billed_sum

            if remaining_price <= Decimal('0'):
                # Allaqachon to'liq oylik narx yechilgan bo'lsa teginmaymiz
                continue

            # Tranzaksiya yaratamiz (monthly_fee - faqat student balansidan kamayadi)
            new_trans = Transaction(
                organization=org,
                account=virtual_account,
                category=category,
                student=student,
                amount=remaining_price,
                transaction_type='monthly_fee',
                status='confirmed',
                created_by=system_user or student,
                confirmed_by=system_user or student,
                confirmed_at=timezone.now(),
                description=(
                    f"{gs.group.name} - {billing_month.strftime('%Y-%m')} oyi uchun "
                    f"to'liq to'lovgacha qolgan qismi ({remaining_price:,.0f} UZS)"
                )
            )
            new_trans.is_auto_billing = True
            new_trans.save()

            total_amount += remaining_price
            billed_count += 1

            self.stdout.write(
                f"  -> {student.first_name} {student.last_name} ({group.name}): "
                f"-{remaining_price:,.0f} UZS qo'shimcha yechildi (To'liq qilingan narx: {full_price:,.0f})."
            )

        if billed_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f"[{org.name}] {billed_count} ta o'quvchidan jami {total_amount:,.0f} UZS yechildi."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(f"[{org.name}] Hamma o'quvchilardan to'liq oylik yechib olingan ekan."))

        # Log yozamiz
        log, _ = MonthlyFeeLog.objects.get_or_create(
            organization=org,
            billing_month=billing_month,
            defaults={'is_processed': True, 'total_students_billed': billed_count, 'total_amount_billed': total_amount}
        )
        if not getattr(log, 'is_new', False):
            log.is_processed = True
            log.processed_at = timezone.now()
            # Billed va amount ustiga qo'shib qo'yamiz
            log.total_students_billed = (log.total_students_billed or 0) + billed_count
            log.total_amount_billed = (log.total_amount_billed or Decimal('0')) + total_amount
            log.save(update_fields=['is_processed', 'processed_at', 'total_students_billed', 'total_amount_billed'])
