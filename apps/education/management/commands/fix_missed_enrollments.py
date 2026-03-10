from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import date
from decimal import Decimal
import calendar

from apps.education.models import GroupStudent
from apps.finance.models import MonthlyFeeLog, TransactionCategory, Account, Transaction
from apps.education.signals import calculate_price_with_bonus, calculate_proportional_price, get_system_user_and_account

class Command(BaseCommand):
    help = "Signal ishlamay qolgan vaqtda qo'shilgan o'quvchilar uchun proporsional to'lovni (orqaga qaytib) hisoblab yechish."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Faqat kimdan qancha yechilishini ko'rsatadi, lekin aslida yechmaydi.",
        )

    def handle(self, *args, **options):
        is_dry_run = options['dry_run']
        today = date.today()
        billing_month = date(today.year, today.month, 1)

        self.stdout.write(self.style.WARNING(f"=== QOLDIRILGAN TO'LOVLARNI YECHISH ({today.strftime('%Y-%m-%d')}) ==="))
        if is_dry_run:
            self.stdout.write(self.style.SUCCESS("*** DRY RUN REJIMI: Tranzaksiyalar yaratilmaydi ***\n"))

        # Barcha faol o'quvchilarni olamiz
        active_gs = GroupStudent.objects.filter(
            status='active',
            student__role='student'
        ).select_related('group__course', 'student', 'group__organization')

        total_billed_amount = Decimal('0')
        students_affected = 0

        with transaction.atomic():
            for gs in active_gs:
                student = gs.student
                group = gs.group
                org = group.organization

                if not org:
                    continue

                # 1. Shu oy uchun tashkilotda hisob-kitob qilinganligini tekshiramiz
                # Agar hisob-kitob hali bo'lmagan bo'lsa, process_monthly_fees o'zi yechadi
                log = MonthlyFeeLog.objects.filter(
                    organization=org,
                    billing_month=billing_month,
                    is_processed=True
                ).first()

                if not log:
                    continue

                # 2. Ushbu studentdan shu oy uchun pul yechilganligini tekshiramiz
                desc_search = f"{group.name} - {billing_month.strftime('%Y-%m')} oyi uchun"
                already_billed = Transaction.objects.filter(
                    student=student,
                    organization=org,
                    transaction_type='monthly_fee',
                    description__contains=desc_search,
                    created_at__year=today.year,
                    created_at__month=today.month
                ).exists()

                if already_billed:
                    continue

                # Student topildi va hali puli yechilmagan!
                # Demak, u hisob-kitob (oy boshi)dan keyin, yoki signal buzilganda qo'shilgan.

                # 3. Kurs narxini olish
                base_price = group.course.price if group.course.price > 0 else Decimal('0')
                if base_price == 0:
                    continue

                # 4. Bonus chegirib, yakuniy to'liq oylik narxni hisoblaymiz
                full_monthly_price = calculate_price_with_bonus(base_price, student)
                if full_monthly_price <= 0:
                    continue

                # 5. Proporsional narxni hisoblaymiz (student QACHON qo'shilganiga qarab)
                joined_date = gs.joined_at
                
                # Agar oldingi oylarda qo'shilgan bo'lsa (lekin nechukdir yechilmagan bo'lsa), 
                # u holda to'liq oy narxi yechiladi. Aks holda, shu oyda qo'shilgan kunidan boshlab proporsional.
                if joined_date.year == today.year and joined_date.month == today.month:
                    calc_day = joined_date.day
                else:
                    calc_day = 1

                total_days = calendar.monthrange(today.year, today.month)[1]
                final_price = calculate_proportional_price(full_monthly_price, calc_day, total_days)

                if final_price <= 0:
                    continue

                students_affected += 1
                total_billed_amount += final_price

                self.stdout.write(
                    f"[TOPILDI] {student.first_name} {student.last_name} | "
                    f"Guruh: {group.name} | "
                    f"Qo'shilgan: {joined_date} | "
                    f"Yechilishi kerak: {final_price:,.0f} UZS"
                )

                if not is_dry_run:
                    category, _ = TransactionCategory.objects.get_or_create(
                        organization=org,
                        name="Kurs to'lovi (Oylik avtomat)",
                        defaults={'transaction_type': 'income'}
                    )

                    system_user, virtual_account = get_system_user_and_account(org)
                    if not virtual_account:
                        self.stdout.write(self.style.ERROR(f"  -> {org.name} uchun virtual kassa topilmadi!"))
                        continue

                    remaining_days = total_days - calc_day + 1
                    desc = (
                        f"{group.name} - {billing_month.strftime('%Y-%m')} oyi uchun to'lov "
                        f"(Qayta tiklangan: {remaining_days}/{total_days} kun, "
                        f"to'liq narx: {full_monthly_price:,.0f} UZS)"
                    )

                    new_trans = Transaction(
                        organization=org,
                        account=virtual_account,
                        category=category,
                        student=student,
                        amount=final_price,
                        transaction_type='monthly_fee',
                        status='confirmed',
                        created_by=system_user or student,
                        confirmed_by=system_user or student,
                        confirmed_at=timezone.now(),
                        description=desc
                    )
                    new_trans.is_auto_billing = True
                    new_trans.save()
                    self.stdout.write(self.style.SUCCESS(f"  -> {final_price:,.0f} UZS yechildi!"))

        if is_dry_run:
            self.stdout.write(self.style.WARNING("\n=== BU DRY RUN EDI. HZCH NIMA O'ZGARIShMADI! ==="))
            self.stdout.write(f"Jami {students_affected} ta o'quvchidan {total_billed_amount:,.0f} UZS yechilishi KUTULMOQDA.")
            self.stdout.write("Haqiqatda yechish uchun: python manage.py fix_missed_enrollments")
        else:
            self.stdout.write(self.style.SUCCESS(f"\n=== YAKUNLANDI ==="))
            self.stdout.write(self.style.SUCCESS(f"Jami {students_affected} ta o'quvchidan {total_billed_amount:,.0f} UZS yechildi!"))
