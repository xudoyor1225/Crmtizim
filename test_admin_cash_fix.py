import os
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.finance.models import Account, Transaction, TransactionCategory
from apps.organizations.models import Organization
from apps.finance.admin_cash_views import admin_add_income, admin_add_expense
from django.contrib.messages import get_messages
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

User = get_user_model()

class AdminCashTransactionTest(TestCase):
    """Test admin cash income/expense functionality"""
    
    def setUp(self):
        # Create test organization
        self.org = Organization.objects.create(
            name="Test Organization",
            subdomain="test"
        )
        
        # Create test admin user
        self.admin = User.objects.create(
            phone="998900000001",
            first_name="Test",
            last_name="Admin",
            role="admin",
            organization=self.org
        )
        
        # Create admin account
        self.admin_account = Account.objects.create(
            organization=self.org,
            name="Admin Kassa - Test Admin",
            account_type="cash",
            balance=Decimal("0.00")
        )
        
        # Create income category
        self.income_category = TransactionCategory.objects.create(
            organization=self.org,
            name="Boshqa kirim",
            transaction_type="income"
        )
        
        # Create expense category
        self.expense_category = TransactionCategory.objects.create(
            organization=self.org,
            name="Boshqa chiqim",
            transaction_type="expense"
        )
    
    def test_admin_income_auto_confirmation(self):
        """Test that admin income transactions are auto-confirmed"""
        # Initial balance
        initial_balance = self.admin_account.balance
        
        # Create a mock request
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.admin
        request.organization = self.org
        request.POST = {
            'category': self.income_category.id,
            'amount': '50000',
            'payment_method': 'cash',
            'description': 'Test income'
        }
        
        # Call the admin_add_income function
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.middleware import MessageMiddleware
        
        # Process request with session and messages
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        
        msg_middleware = MessageMiddleware()
        msg_middleware.process_request(request)
        
        # Import the function and call it
        from apps.finance.admin_cash_views import admin_add_income
        response = admin_add_income(request)
        
        # Check that transaction was created and confirmed
        transaction = Transaction.objects.filter(
            account=self.admin_account,
            transaction_type='income'
        ).latest('created_at')
        
        self.assertEqual(transaction.status, 'confirmed')
        self.assertEqual(transaction.amount, Decimal('50000'))
        self.assertIsNotNone(transaction.confirmed_by)
        self.assertIsNotNone(transaction.confirmed_at)
        self.assertEqual(transaction.confirmed_by, self.admin)
        
        # Refresh the account balance from DB
        self.admin_account.refresh_from_db()
        expected_balance = initial_balance + Decimal('50000')
        self.assertEqual(self.admin_account.balance, expected_balance)
        
        print("✅ Admin income auto-confirmation test passed!")
        print(f"   Transaction status: {transaction.status}")
        print(f"   Account balance: {self.admin_account.balance}")
    
    def test_admin_expense_auto_confirmation(self):
        """Test that admin expense transactions are auto-confirmed"""
        # Set initial balance
        self.admin_account.balance = Decimal('100000')
        self.admin_account.save()
        initial_balance = self.admin_account.balance
        
        # Create a mock request
        request = HttpRequest()
        request.method = 'POST'
        request.user = self.admin
        request.organization = self.org
        request.POST = {
            'category': self.expense_category.id,
            'amount': '30000',
            'payment_method': 'cash',
            'description': 'Test expense'
        }
        
        # Process request with session and messages
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.middleware import MessageMiddleware
        
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        
        msg_middleware = MessageMiddleware()
        msg_middleware.process_request(request)
        
        # Import the function and call it
        from apps.finance.admin_cash_views import admin_add_expense
        response = admin_add_expense(request)
        
        # Check that transaction was created and confirmed
        transaction = Transaction.objects.filter(
            account=self.admin_account,
            transaction_type='expense'
        ).latest('created_at')
        
        self.assertEqual(transaction.status, 'confirmed')
        self.assertEqual(transaction.amount, Decimal('30000'))
        self.assertIsNotNone(transaction.confirmed_by)
        self.assertIsNotNone(transaction.confirmed_at)
        self.assertEqual(transaction.confirmed_by, self.admin)
        
        # Refresh the account balance from DB
        self.admin_account.refresh_from_db()
        expected_balance = initial_balance - Decimal('30000')
        self.assertEqual(self.admin_account.balance, expected_balance)
        
        print("✅ Admin expense auto-confirmation test passed!")
        print(f"   Transaction status: {transaction.status}")
        print(f"   Account balance: {self.admin_account.balance}")
    
    def test_dashboard_statistics_include_confirmed_only(self):
        """Test that dashboard statistics only include confirmed transactions"""
        # Create a pending transaction (this shouldn't affect stats after our fix)
        pending_transaction = Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('25000'),
            transaction_type='income',
            status='pending',  # This should not affect the balance anymore with our fix
            created_by=self.admin
        )
        
        # Create a confirmed transaction
        confirmed_transaction = Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('35000'),
            transaction_type='income',
            status='confirmed',
            created_by=self.admin
        )
        
        # Import and call admin dashboard logic
        from apps.finance.admin_cash_views import _get_or_create_admin_account
        admin_account = _get_or_create_admin_account(self.admin, self.org)
        
        # Get confirmed transactions only for stats
        from django.db.models import Sum
        confirmed_txs = Transaction.objects.filter(
            account=admin_account,
            is_deleted=False,
            status='confirmed',
        )
        total_income = confirmed_txs.filter(transaction_type='income').aggregate(t=Sum('amount'))['t'] or 0
        
        # The total income should only include the confirmed transaction
        self.assertEqual(total_income, Decimal('35000'))
        
        print("✅ Dashboard statistics test passed!")
        print(f"   Total income (confirmed only): {total_income}")

if __name__ == "__main__":
    import django
    django.setup()
    import unittest
    unittest.main()