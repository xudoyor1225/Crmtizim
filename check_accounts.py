import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.finance.models import Account

for acc in Account.objects.all():
    print(acc.id, acc.name, acc.account_type, acc.balance)
