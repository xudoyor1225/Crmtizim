import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.finance.models import Transaction

# Get the last added student to inspect
u = User.objects.filter(role='student').order_by('-id').first()
if getattr(u, 'uid', None):
    print("Test Student:", u.full_name, "Balance before:", u.balance)
    print("Transactions:")
    for t in Transaction.objects.filter(student=u).order_by('-created_at')[:5]:
        print(f" - {t.amount} {t.transaction_type} {t.status}: {t.description}")
        
    print("Wait, checking all students to see if ANY went negative...")
    negatives = User.objects.filter(role='student', balance__lt=0).count()
    print("Number of negative balance students:", negatives)
    if negatives > 0:
        first_neg = User.objects.filter(role='student', balance__lt=0).first()
        print("First negative student:", first_neg.full_name, "Balance:", first_neg.balance)
else:
    print("No students found.")
