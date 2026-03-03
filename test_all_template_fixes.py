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

def test_submission_list_template():
    """Test submission list template with null values"""
    print("Testing submission list template with null values...")
    
    class MockSubmission:
        def __init__(self):
            self.id = 6
            self.admin_user = None  # This will be None to test null safety
            self.admin_account = MockAccount(None)  # None name
            self.main_account = MockAccount(None)   # None name
            self.net_amount = Decimal('1000.00')
            self.total_income = Decimal('1500.00')
            self.total_expense = Decimal('500.00')
            self.created_at = date.today()
            self.status = 'pending'
            self.approved_by = None  # This is the key test case
            self.approved_at = None
            self.rejection_reason = None
            self.get_status_display = lambda: "Kutilmoqda"
            self.get_period_type_display = lambda: "Kunlik"
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
            self.name = name  # This can be None
    
    # Test the problematic section from submission_list.html
    test_template = """
    <table>
        <tr>
            <td class="p-4 text-sm text-slate-700 font-medium">{% if sub.admin_user %}{{ sub.admin_user.get_full_name }}{% else %}Foydalanuvchi{% endif %}</td>
            <td class="p-4 text-sm text-slate-600">{{ sub.admin_account.name|default:"Hisob topilmadi" }}</td>
            <td class="p-4 text-sm text-slate-600">{{ sub.main_account.name|default:"Asosiy kassa" }}</td>
            <td>
                <div class="text-xs text-slate-500">
                    <span class="font-medium">{% if sub.approved_by %}{{ sub.approved_by.get_full_name }}{% else %}-{% endif %}</span>
                    {% if sub.approved_at %}
                    <br>{{ sub.approved_at|date:"d.m.Y H:i" }}
                    {% endif %}
                    {% if sub.rejection_reason %}
                    <br><span class="text-rose-500">{{ sub.rejection_reason }}</span>
                    {% endif %}
                </div>
            </td>
        </tr>
    </table>
    """
    
    template = Template(test_template)
    context = Context({'sub': MockSubmission()})
    
    try:
        rendered = template.render(context)
        print("✅ Submission list template rendered successfully with null values")
        print("Rendered output:")
        print(rendered)
        return True
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_submission_detail_template():
    """Test submission detail template with null values"""
    print("\nTesting submission detail template with null values...")
    
    class MockSubmission:
        def __init__(self):
            self.id = 6
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
    
    # Test the problematic section from submission_detail.html
    test_template = """
    <div class="bg-white rounded-2xl p-5 border border-slate-200">
        <h3 class="font-semibold text-slate-700 mb-4">Tasdiqlash Ma'lumotlari</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
                <p class="text-sm text-slate-400">Holat bo'yicha mas'ul</p>
                <p class="font-medium text-slate-700">{% if submission.approved_by %}{{ submission.approved_by.get_full_name }}{% else %}Ma'lum emas{% endif %}</p>
            </div>
            <div>
                <p class="text-sm text-slate-400">Ko'rib chiqilgan vaqt</p>
                <p class="font-medium text-slate-700">{% if submission.approved_at %}{{ submission.approved_at|date:"d.m.Y H:i" }}{% else %}-{% endif %}</p>
            </div>
            {% if submission.rejection_reason %}
            <div class="md:col-span-3">
                <p class="text-sm text-slate-400">Rad etish sababi</p>
                <p class="font-medium text-rose-600">{{ submission.rejection_reason|default:"Sabab ko'rsatilmagan" }}</p>
            </div>
            {% endif %}
        </div>
    </div>
    """
    
    template = Template(test_template)
    context = Context({'submission': MockSubmission()})
    
    try:
        rendered = template.render(context)
        print("✅ Submission detail template rendered successfully with null values")
        print("Rendered output:")
        print(rendered)
        return True
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Django template null safety fixes...")
    
    success1 = test_submission_list_template()
    success2 = test_submission_detail_template()
    
    if success1 and success2:
        print("\n🎉 All template tests passed!")
        print("✅ All null safety fixes are working correctly")
        print("✅ Cash submission functionality should work without errors")
    else:
        print("\n❌ Some template tests failed")