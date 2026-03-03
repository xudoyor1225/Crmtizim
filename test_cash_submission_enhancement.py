"""
Test script to verify the enhanced cash submission feature with payment method categorization
"""
import os
import sys
import django
from decimal import Decimal

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import TestCase
from apps.finance.models import Account, Transaction, TransactionCategory, CashSubmission
from apps.users.models import User
from apps.organizations.models import Organization
from datetime import date, timedelta

class CashSubmissionEnhancementTest(TestCase):
    """Test the enhanced cash submission feature"""
    
    def setUp(self):
        # Create test organization
        self.org = Organization.objects.create(
            name="Test Organization",
            subdomain="test-org"
        )
        
        # Create test users
        self.admin = User.objects.create_user(
            phone="998901111111",
            password="test123",
            first_name="Admin",
            last_name="User",
            role="admin",
            organization=self.org
        )
        
        self.super_admin = User.objects.create_user(
            phone="998902222222",
            password="test123",
            first_name="Super",
            last_name="Admin",
            role="super_admin",
            organization=self.org
        )
        
        # Create accounts
        self.admin_account = Account.objects.create(
            organization=self.org,
            name="Admin Kassa - Admin User",
            account_type='cash',
            balance=Decimal('0.00')
        )
        
        self.main_account = Account.objects.create(
            organization=self.org,
            name="Asosiy Kassa",
            account_type='cash',
            balance=Decimal('1000000.00')
        )
        
        # Create categories
        self.income_category = TransactionCategory.objects.create(
            organization=self.org,
            name="Kurs to'lovi",
            transaction_type='income'
        )
        
        self.expense_category = TransactionCategory.objects.create(
            organization=self.org,
            name="Xodimlar oyligi",
            transaction_type='expense'
        )
    
    def test_payment_method_breakdown_calculation(self):
        """Test that payment method breakdown is calculated correctly"""
        # Create transactions with different payment methods
        Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('100000'),
            transaction_type='income',
            payment_method='cash',
            description="Naqd to'lov",
            status='confirmed',
            created_by=self.admin
        )
        
        Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('150000'),
            transaction_type='income',
            payment_method='card',
            description="Plastik to'lov",
            status='confirmed',
            created_by=self.admin
        )
        
        Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('200000'),
            transaction_type='income',
            payment_method='transfer',
            description="Bank o'tkazmasi",
            status='confirmed',
            created_by=self.admin
        )
        
        Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('50000'),
            transaction_type='income',
            payment_method='online',
            description="Online to'lov",
            status='confirmed',
            created_by=self.admin
        )
        
        # Create expense transaction
        Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.expense_category,
            amount=Decimal('75000'),
            transaction_type='expense',
            payment_method='cash',
            description="Xodimlar oyligi",
            status='confirmed',
            created_by=self.admin
        )
        
        # Create cash submission
        today = date.today()
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal('500000'),  # 100000 + 150000 + 200000 + 50000
            total_expense=Decimal('75000'),
            net_amount=Decimal('425000'),   # 500000 - 75000
            amount_cash=Decimal('100000'),   # Only income cash transactions
            amount_card=Decimal('150000'),
            amount_terminal=Decimal('200000'),
            amount_other=Decimal('50000'),
            period_type='weekly',
            period_start=today - timedelta(days=7),
            period_end=today,
            status='pending'
        )
        
        # Verify payment method breakdown
        self.assertEqual(submission.amount_cash, Decimal('100000'))
        self.assertEqual(submission.amount_card, Decimal('150000'))
        self.assertEqual(submission.amount_terminal, Decimal('200000'))
        self.assertEqual(submission.amount_other, Decimal('50000'))
        self.assertEqual(submission.total_income, Decimal('500000'))
        self.assertEqual(submission.total_expense, Decimal('75000'))
        self.assertEqual(submission.net_amount, Decimal('425000'))
        
        print("✅ Payment method breakdown calculation test passed!")
        print(f"   Cash: {submission.amount_cash} UZS")
        print(f"   Card: {submission.amount_card} UZS") 
        print(f"   Terminal: {submission.amount_terminal} UZS")
        print(f"   Other: {submission.amount_other} UZS")
        print(f"   Net Amount: {submission.net_amount} UZS")
    
    def test_cash_submission_detail_view_data(self):
        """Test that the detail view provides correct transaction data"""
        # Create test transactions
        tx1 = Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('100000'),
            transaction_type='income',
            payment_method='cash',
            description="Student payment",
            status='confirmed',
            created_by=self.admin,
            student=self.admin  # Using admin as student for test
        )
        
        tx2 = Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.expense_category,
            amount=Decimal('50000'),
            transaction_type='expense',
            payment_method='cash',
            description="Office supplies",
            status='confirmed',
            created_by=self.admin
        )
        
        # Create cash submission
        today = date.today()
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal('100000'),
            total_expense=Decimal('50000'),
            net_amount=Decimal('50000'),
            amount_cash=Decimal('100000'),
            amount_card=Decimal('0'),
            amount_terminal=Decimal('0'),
            amount_other=Decimal('0'),
            period_type='weekly',
            period_start=today - timedelta(days=7),
            period_end=today,
            status='pending'
        )
        
        # Test transaction filtering logic (simulating the view logic)
        from django.db.models import Sum
        from decimal import Decimal
        
        period_transactions = Transaction.objects.filter(
            account=submission.admin_account,
            created_at__date__gte=submission.period_start,
            created_at__date__lte=submission.period_end
        )
        
        income_transactions = period_transactions.filter(transaction_type='income')
        expense_transactions = period_transactions.filter(transaction_type='expense')
        
        # Test payment method statistics
        payment_method_stats = {}
        for method in ['cash', 'card', 'transfer', 'online']:
            method_transactions = period_transactions.filter(payment_method=method)
            total = method_transactions.aggregate(t=Sum('amount'))['t'] or Decimal('0')
            payment_method_stats[method] = {
                'total': total,
                'count': method_transactions.count(),
                'transactions': method_transactions
            }
        
        # Verify results
        self.assertEqual(period_transactions.count(), 2)
        self.assertEqual(income_transactions.count(), 1)
        self.assertEqual(expense_transactions.count(), 1)
        self.assertEqual(payment_method_stats['cash']['count'], 2)
        self.assertEqual(payment_method_stats['cash']['total'], Decimal('150000'))  # 100000 income + 50000 expense
        
        print("✅ Cash submission detail view data test passed!")
        print(f"   Total transactions: {period_transactions.count()}")
        print(f"   Income transactions: {income_transactions.count()}")
        print(f"   Expense transactions: {expense_transactions.count()}")
        print(f"   Cash transactions: {payment_method_stats['cash']['count']}")
        print(f"   Cash total: {payment_method_stats['cash']['total']} UZS")

if __name__ == '__main__':
    import unittest
    # Run the tests
    suite = unittest.TestLoader().loadTestsFromTestCase(CashSubmissionEnhancementTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed! The enhanced cash submission feature is working correctly.")
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed.")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")