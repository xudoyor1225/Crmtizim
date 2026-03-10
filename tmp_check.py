import sys
import os

# Ensure the project root is in Python's path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()

from apps.education.models import GroupStudent
from datetime import date
from decimal import Decimal
from apps.finance.models import MonthlyFeeLog, TransactionCategory, Account, Transaction
from apps.users.models import User
import calendar
from apps.education.signals import calculate_price_with_bonus, calculate_proportional_price, get_system_user_and_account

gs_list = GroupStudent.objects.order_by('-id')[:5]
for gs in gs_list:
    student = gs.student
    group = gs.group
    org = group.organization

    print(f'\n--- Checking GS: {gs.id}, Student: {student.first_name}, Org: {org.name} ---')

    if gs.status != 'active':
        print('Returned: Not active')
        continue

    today = date.today()
    billing_month = date(today.year, today.month, 1)

    log = MonthlyFeeLog.objects.filter(
        organization=org,
        billing_month=billing_month,
        is_processed=True
    ).first()

    if not log:
        print('Returned: No MonthlyFeeLog')
        continue

    desc_search = f'{group.name} - {billing_month.strftime("%Y-%m")} oyi uchun'
    already_billed = Transaction.objects.filter(
        student=student,
        organization=org,
        transaction_type='monthly_fee',
        description__contains=desc_search,
        created_at__year=today.year,
        created_at__month=today.month
    ).exists()

    if already_billed:
        print('Returned: Already billed')
        continue

    base_price = group.course.price if group.course.price > 0 else Decimal('0')
    if base_price == 0:
        print('Returned: Course price is 0')
        continue

    full_monthly_price = calculate_price_with_bonus(base_price, student)
    if full_monthly_price <= 0:
        print('Returned: full_monthly_price <= 0')
        continue

    total_days = calendar.monthrange(today.year, today.month)[1]
    final_price = calculate_proportional_price(full_monthly_price, today.day, total_days)

    if final_price <= 0:
        print('Returned: final_price <= 0')
        continue

    system_user, virtual_account = get_system_user_and_account(org)
    if not virtual_account:
        print('Returned: No virtual account')
        continue

    print('All checks passed! Signal WOULD have created the transaction.')
