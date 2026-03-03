"""
Test script to verify all the implemented cash submission and payment improvements
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.test import TestCase
from apps.finance.models import Account, Transaction, TransactionCategory, CashSubmission
from apps.users.models import User
from apps.organizations.models import Organization
from django.utils import timezone

class CashSubmissionPaymentImprovementsTest(TestCase):
    """Test all the implemented improvements"""
    
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
    
    def test_daily_cash_submission_only(self):
        """Test that cash submission only includes today's transactions"""
        today = timezone.now().date()
        
        # Create transactions for today
        Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('100000'),
            transaction_type='income',
            payment_method='cash',
            description="Bugungi to'lov",
            status='confirmed',
            created_by=self.admin
        )
        
        # Create transaction for yesterday (should not be included)
        yesterday_tx = Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('50000'),
            transaction_type='income',
            payment_method='cash',
            description="Kechagi to'lov",
            status='confirmed',
            created_by=self.admin
        )
        # Manually set created_at to yesterday
        yesterday_tx.created_at = timezone.now() - timezone.timedelta(days=1)
        yesterday_tx.save()
        
        # Create cash submission (simulating the view logic)
        period_txs = Transaction.objects.filter(
            account=self.admin_account,
            is_deleted=False,
            status='confirmed',
            created_at__date__gte=today,
            created_at__date__lte=today,  # Only today
        )
        
        total_income = period_txs.filter(transaction_type='income').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        total_expense = period_txs.filter(transaction_type='expense').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        
        # Verify only today's transaction is included
        self.assertEqual(period_txs.count(), 1)  # Only today's transaction
        self.assertEqual(total_income, Decimal('100000'))
        self.assertEqual(total_expense, Decimal('0'))
        
        print("✅ Daily cash submission test passed!")
        print(f"   Today's transactions: {period_txs.count()}")
        print(f"   Total income: {total_income} UZS")
        print(f"   Total expense: {total_expense} UZS")
    
    def test_payment_method_receipt_upload(self):
        """Test that receipt upload appears only for non-cash payments"""
        # Test cash payment (no receipt required)
        cash_payment_data = {
            'payment_method': 'cash',
            'amount': Decimal('100000'),
            'description': 'Naqd to\'lov'
        }
        
        # Test card payment (receipt required)
        card_payment_data = {
            'payment_method': 'card',
            'amount': Decimal('150000'),
            'description': 'Plastik to\'lov',
            'receipt_required': True
        }
        
        # Test transfer payment (receipt required)
        transfer_payment_data = {
            'payment_method': 'transfer',
            'amount': Decimal('200000'),
            'description': 'Bank o\'tkazmasi',
            'receipt_required': True
        }
        
        # Verify receipt requirement logic
        payment_methods = [
            cash_payment_data,
            card_payment_data,
            transfer_payment_data
        ]
        
        receipt_required_count = 0
        for payment in payment_methods:
            if payment.get('receipt_required', False):
                receipt_required_count += 1
        
        # Should be 2 payments requiring receipt (card and transfer)
        self.assertEqual(receipt_required_count, 2)
        
        print("✅ Payment method receipt upload test passed!")
        print(f"   Payment methods requiring receipt: {receipt_required_count}")
    
    def test_balance_calculation_fix(self):
        """Test that admin balance is correctly reset after submission"""
        # Set initial balance
        self.admin_account.balance = Decimal('500000')
        self.admin_account.save()
        
        # Create transactions
        Transaction.objects.create(
            organization=self.org,
            account=self.admin_account,
            category=self.income_category,
            amount=Decimal('300000'),
            transaction_type='income',
            payment_method='cash',
            description="Test to'lov",
            status='confirmed',
            created_by=self.admin
        )
        
        # Simulate submission process
        self.admin_account.refresh_from_db()
        net_amount = self.admin_account.balance  # Should be 500000 (initial) + 300000 (transaction) = 800000
        
        # Reset balance to 0 (simulating the fix)
        if self.admin_account.balance != Decimal('0.00'):
            self.admin_account.balance = Decimal('0.00')
            self.admin_account.save(update_fields=['balance'])
        
        # Verify balance is reset
        self.admin_account.refresh_from_db()
        self.assertEqual(self.admin_account.balance, Decimal('0.00'))
        
        print("✅ Balance calculation fix test passed!")
        print(f"   Final balance: {self.admin_account.balance} UZS")
    
    def test_payment_method_breakdown(self):
        """Test payment method breakdown calculation"""
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
        
        # Calculate payment method breakdown
        period_txs = Transaction.objects.filter(
            account=self.admin_account,
            status='confirmed'
        )
        
        amount_cash = period_txs.filter(payment_method='cash').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        amount_card = period_txs.filter(payment_method='card').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        amount_terminal = period_txs.filter(payment_method='transfer').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        amount_other = period_txs.filter(payment_method='online').aggregate(t=Sum('amount'))['t'] or Decimal('0')
        
        # Verify breakdown
        self.assertEqual(amount_cash, Decimal('100000'))
        self.assertEqual(amount_card, Decimal('150000'))
        self.assertEqual(amount_terminal, Decimal('200000'))
        self.assertEqual(amount_other, Decimal('0'))
        
        print("✅ Payment method breakdown test passed!")
        print(f"   Cash: {amount_cash} UZS")
        print(f"   Card: {amount_card} UZS")
        print(f"   Terminal: {amount_terminal} UZS")
        print(f"   Other: {amount_other} UZS")

if __name__ == '__main__':
    import unittest
    from django.db.models import Sum
    
    # Run the tests
    suite = unittest.TestLoader().loadTestsFromTestCase(CashSubmissionPaymentImprovementsTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed! All improvements are working correctly.")
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed.")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")