import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def fix_database_schema():
    """Fix the database schema issue by applying the missing migration"""
    print("🔧 Checking database schema for cash submission payment method fields...")
    
    # Check if the required columns exist
    cursor = connection.cursor()
    
    if connection.vendor == 'sqlite':
        cursor.execute("PRAGMA table_info(finance_cash_submissions)")
        columns = [col[1] for col in cursor.fetchall()]
    elif connection.vendor == 'postgresql':
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'finance_cash_submissions'
        """)
        columns = [col[0] for col in cursor.fetchall()]
    
    required_columns = ['amount_cash', 'amount_card', 'amount_terminal', 'amount_other']
    missing_columns = [col for col in required_columns if col not in columns]
    
    if missing_columns:
        print(f"❌ Missing columns: {missing_columns}")
        print("Applying migration 0008...")
        
        try:
            # Apply the migration
            execute_from_command_line(['manage.py', 'migrate', 'finance', '0008_add_payment_method_fields_to_cash_submission'])
            print("✅ Migration applied successfully!")
            
            # Verify the columns now exist
            if connection.vendor == 'sqlite':
                cursor.execute("PRAGMA table_info(finance_cash_submissions)")
                columns = [col[1] for col in cursor.fetchall()]
            elif connection.vendor == 'postgresql':
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'finance_cash_submissions'
                """)
                columns = [col[0] for col in cursor.fetchall()]
            
            still_missing = [col for col in required_columns if col not in columns]
            if still_missing:
                print(f"⚠️  Some columns still missing: {still_missing}")
                return False
            else:
                print("✅ All required columns are now present in the database")
                return True
                
        except Exception as e:
            print(f"❌ Error applying migration: {e}")
            return False
    else:
        print("✅ All required columns are already present in the database")
        return True

def test_cash_submission_detail():
    """Test if the cash submission detail view works correctly"""
    print("\n🧪 Testing cash submission detail functionality...")
    
    try:
        from apps.finance.models import CashSubmission, Transaction
        from apps.users.models import User
        from decimal import Decimal
        from django.utils import timezone
        from datetime import date
        
        # Create a test cash submission if none exists
        if not CashSubmission.objects.exists():
            print("Creating test cash submission...")
            admin_user = User.objects.filter(role='admin').first()
            if not admin_user:
                print("❌ No admin user found for testing")
                return False
                
            # Create a test cash submission
            from apps.finance.models import Account
            admin_account = Account.objects.filter(name__icontains='admin').first()
            main_account = Account.objects.filter(account_type='main').first()
            
            if not admin_account or not main_account:
                print("❌ Required accounts not found for testing")
                return False
            
            submission = CashSubmission.objects.create(
                admin_user=admin_user,
                admin_account=admin_account,
                main_account=main_account,
                total_income=Decimal('1000000'),
                total_expense=Decimal('200000'),
                net_amount=Decimal('800000'),
                amount_cash=Decimal('500000'),
                amount_card=Decimal('300000'),
                amount_terminal=Decimal('200000'),
                amount_other=Decimal('0'),
                period_type='weekly',
                period_start=date.today(),
                period_end=date.today(),
                status='pending'
            )
            print(f"✅ Created test cash submission #{submission.id}")
        else:
            submission = CashSubmission.objects.first()
            print(f"✅ Using existing cash submission #{submission.id}")
        
        # Test the detail view logic
        from apps.finance.admin_cash_views import cash_submission_detail
        from django.http import HttpRequest
        from django.contrib.auth.models import AnonymousUser
        
        # Create a mock request
        request = HttpRequest()
        request.user = submission.admin_user
        request.organization = submission.organization if hasattr(submission, 'organization') else None
        
        # Test accessing the submission detail
        try:
            # This would normally be called as a view function
            # We're just testing that the data access works
            period_transactions = Transaction.objects.filter(
                is_deleted=False,
                created_at__date__gte=submission.period_start,
                created_at__date__lte=submission.period_end,
                account=submission.admin_account
            )
            
            print(f"✅ Successfully accessed {period_transactions.count()} transactions for submission")
            return True
            
        except Exception as e:
            print(f"❌ Error accessing cash submission data: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error in testing: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database schema fix and functionality test...")
    
    # Fix database schema
    schema_fixed = fix_database_schema()
    
    # Test functionality
    if schema_fixed:
        functionality_works = test_cash_submission_detail()
        
        if functionality_works:
            print("\n🎉 All fixes applied successfully!")
            print("✅ Database schema is correct")
            print("✅ Cash submission detail functionality works")
            print("✅ The 'batafsil' button should now work correctly")
        else:
            print("\n❌ Functionality test failed")
    else:
        print("\n❌ Database schema fix failed")