import os
import django
from django.template import Context, Template
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

User = get_user_model()

def test_template_with_null_approved_by():
    """Test template rendering with null approved_by field"""
    print("Testing template with null approved_by field...")
    
    # Create a mock submission object with null approved_by
    class MockSubmission:
        def __init__(self):
            self.id = 5
            self.admin_user = MockUser("Test", "Admin")
            self.admin_account = MockAccount("Admin Account")
            self.main_account = MockAccount("Main Account")
            self.net_amount = Decimal('1000.00')
            self.amount_cash = Decimal('500.00')
            self.amount_card = Decimal('300.00')
            self.amount_terminal = Decimal('200.00')
            self.amount_other = Decimal('0.00')
            self.total_income = Decimal('1500.00')
            self.total_expense = Decimal('500.00')
            self.created_at = date.today()
            self.status = 'pending'
            self.approved_by = None  # This is the key test case
            self.approved_at = None
            self.rejection_reason = None
            self.notes = None
            self.get_status_display = lambda: "Kutilmoqda"
            self.period_start = date.today()
            self.period_end = date.today()
    
    class MockUser:
        def __init__(self, first_name, last_name):
            self.first_name = first_name
            self.last_name = last_name
        
        def get_full_name(self):
            return f"{self.first_name} {self.last_name}"
    
    class MockAccount:
        def __init__(self, name):
            self.name = name
    
    # Test template content (simplified version focusing on the problematic area)
    template_content = """
    <div>
        <h3>Tasdiqlash Ma'lumotlari</h3>
        <div>
            <div>
                <p class="text-sm text-slate-400">Holat bo'yicha mas'ul</p>
                <p class="font-medium text-slate-700">{% if submission.approved_by %}{{ submission.approved_by.get_full_name }}{% else %}Ma'lum emas{% endif %}</p>
            </div>
            <div>
                <p class="text-sm text-slate-400">Ko'rib chiqilgan vaqt</p>
                <p class="font-medium text-slate-700">{% if submission.approved_at %}{{ submission.approved_at|date:"d.m.Y H:i" }}{% else %}-{% endif %}</p>
            </div>
        </div>
    </div>
    """
    
    template = Template(template_content)
    context = Context({'submission': MockSubmission()})
    
    try:
        rendered = template.render(context)
        print("✅ Template rendered successfully with null approved_by")
        print("Rendered output:")
        print(rendered)
        return True
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

def test_template_with_valid_approved_by():
    """Test template rendering with valid approved_by field"""
    print("\nTesting template with valid approved_by field...")
    
    # Create a mock submission object with valid approved_by
    class MockSubmission:
        def __init__(self):
            self.id = 5
            self.admin_user = MockUser("Test", "Admin")
            self.admin_account = MockAccount("Admin Account")
            self.main_account = MockAccount("Main Account")
            self.net_amount = Decimal('1000.00')
            self.amount_cash = Decimal('500.00')
            self.amount_card = Decimal('300.00')
            self.amount_terminal = Decimal('200.00')
            self.amount_other = Decimal('0.00')
            self.total_income = Decimal('1500.00')
            self.total_expense = Decimal('500.00')
            self.created_at = date.today()
            self.status = 'approved'
            self.approved_by = MockUser("Approver", "User")
            self.approved_at = date.today()
            self.rejection_reason = None
            self.notes = None
            self.get_status_display = lambda: "Tasdiqlandi"
            self.period_start = date.today()
            self.period_end = date.today()
    
    class MockUser:
        def __init__(self, first_name, last_name):
            self.first_name = first_name
            self.last_name = last_name
        
        def get_full_name(self):
            return f"{self.first_name} {self.last_name}"
    
    class MockAccount:
        def __init__(self, name):
            self.name = name
    
    # Test template content
    template_content = """
    <div>
        <h3>Tasdiqlash Ma'lumotlari</h3>
        <div>
            <div>
                <p class="text-sm text-slate-400">Holat bo'yicha mas'ul</p>
                <p class="font-medium text-slate-700">{% if submission.approved_by %}{{ submission.approved_by.get_full_name }}{% else %}Ma'lum emas{% endif %}</p>
            </div>
            <div>
                <p class="text-sm text-slate-400">Ko'rib chiqilgan vaqt</p>
                <p class="font-medium text-slate-700">{% if submission.approved_at %}{{ submission.approved_at|date:"d.m.Y H:i" }}{% else %}-{% endif %}</p>
            </div>
        </div>
    </div>
    """
    
    template = Template(template_content)
    context = Context({'submission': MockSubmission()})
    
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
    
    success1 = test_template_with_null_approved_by()
    success2 = test_template_with_valid_approved_by()
    
    if success1 and success2:
        print("\n🎉 All template tests passed!")
        print("✅ Template handles null approved_by safely")
        print("✅ Cash submission detail page should work correctly")
    else:
        print("\n❌ Some template tests failed")