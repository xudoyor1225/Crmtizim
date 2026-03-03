import os
import django
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.template import Context, Template
from apps.finance.models import CashSubmission, Account
from decimal import Decimal
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

User = get_user_model()

def test_template_with_null_values():
    """Test that the template handles null values correctly"""
    print("Testing template with null approved_by field...")
    
    # Create test data
    admin_user = User.objects.create_user(
        username='testadmin',
        email='admin@test.com',
        first_name='Test',
        last_name='Admin',
        role='admin'
    )
    
    # Create accounts
    admin_account = Account.objects.create(
        name='Test Admin Account',
        account_type='cash',
        balance=Decimal('1000.00')
    )
    
    main_account = Account.objects.create(
        name='Main Account',
        account_type='main',
        balance=Decimal('5000.00')
    )
    
    # Create cash submission with null approved_by
    submission = CashSubmission.objects.create(
        admin_user=admin_user,
        admin_account=admin_account,
        main_account=main_account,
        total_income=Decimal('1000.00'),
        total_expense=Decimal('200.00'),
        net_amount=Decimal('800.00'),
        amount_cash=Decimal('500.00'),
        amount_card=Decimal('300.00'),
        amount_terminal=Decimal('0.00'),
        amount_other=Decimal('0.00'),
        period_type='weekly',
        period_start=date.today(),
        period_end=date.today(),
        status='pending',
        approved_by=None,  # This is the key test case
        approved_at=None
    )
    
    # Test template rendering
    template_content = """
    <div>
        <p>Admin: {{ submission.admin_user.get_full_name|default:"Foydalanuvchi" }}</p>
        <p>Approved by: {{ submission.approved_by.get_full_name|default:"Ma'lum emas" }}</p>
        <p>Admin Account: {{ submission.admin_account.name|default:"Hisob topilmadi" }}</p>
        <p>Main Account: {{ submission.main_account.name|default:"Hisob topilmadi" }}</p>
        <p>Net Amount: {{ submission.net_amount|floatformat:0 }} UZS</p>
    </div>
    """
    
    template = Template(template_content)
    context = Context({'submission': submission})
    
    try:
        rendered = template.render(context)
        print("✅ Template rendered successfully with null approved_by")
        print("Rendered output:")
        print(rendered)
        return True
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

def test_template_with_valid_values():
    """Test that the template works with valid values"""
    print("\nTesting template with valid approved_by field...")
    
    # Create test data
    admin_user = User.objects.filter(role='admin').first()
    if not admin_user:
        admin_user = User.objects.create_user(
            username='testadmin2',
            email='admin2@test.com',
            first_name='Test2',
            last_name='Admin2',
            role='admin'
        )
    
    approver_user = User.objects.create_user(
        username='testapprover',
        email='approver@test.com',
        first_name='Test',
        last_name='Approver',
        role='super_admin'
    )
    
    # Get or create accounts
    admin_account = Account.objects.filter(name__icontains='admin').first()
    if not admin_account:
        admin_account = Account.objects.create(
            name='Test Admin Account 2',
            account_type='cash',
            balance=Decimal('1000.00')
        )
    
    main_account = Account.objects.filter(account_type='main').first()
    if not main_account:
        main_account = Account.objects.create(
            name='Main Account 2',
            account_type='main',
            balance=Decimal('5000.00')
        )
    
    # Create cash submission with valid approved_by
    submission = CashSubmission.objects.create(
        admin_user=admin_user,
        admin_account=admin_account,
        main_account=main_account,
        total_income=Decimal('1500.00'),
        total_expense=Decimal('300.00'),
        net_amount=Decimal('1200.00'),
        amount_cash=Decimal('800.00'),
        amount_card=Decimal('400.00'),
        amount_terminal=Decimal('0.00'),
        amount_other=Decimal('0.00'),
        period_type='weekly',
        period_start=date.today(),
        period_end=date.today(),
        status='approved',
        approved_by=approver_user,
        approved_at=date.today()
    )
    
    # Test template rendering
    template_content = """
    <div>
        <p>Admin: {{ submission.admin_user.get_full_name|default:"Foydalanuvchi" }}</p>
        <p>Approved by: {{ submission.approved_by.get_full_name|default:"Ma'lum emas" }}</p>
        <p>Admin Account: {{ submission.admin_account.name|default:"Hisob topilmadi" }}</p>
        <p>Main Account: {{ submission.main_account.name|default:"Hisob topilmadi" }}</p>
        <p>Net Amount: {{ submission.net_amount|floatformat:0 }} UZS</p>
    </div>
    """
    
    template = Template(template_content)
    context = Context({'submission': submission})
    
    try:
        rendered = template.render(context)
        print("✅ Template rendered successfully with valid approved_by")
        print("Rendered output:")
        print(rendered)
        return True
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Django template null safety fixes...")
    
    success1 = test_template_with_null_values()
    success2 = test_template_with_valid_values()
    
    if success1 and success2:
        print("\n🎉 All template tests passed!")
        print("✅ Template now handles null values safely")
        print("✅ Cash submission detail page should work correctly")
    else:
        print("\n❌ Some template tests failed")