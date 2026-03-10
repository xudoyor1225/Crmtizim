import os
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from apps.finance.models import Account, Transaction, TransactionCategory
from apps.organizations.models import Organization
from apps.core.dashboards import super_admin_dashboard

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

User = get_user_model()

class DashboardCalculationTest(TestCase):
    """Test dashboard financial calculation logic"""
    
    def setUp(self):
        # Create test organization
        self.org = Organization.objects.create(
            name="Test Organization",
            subdomain="test"
        )
        
        # Create test users
        self.super_admin = User.objects.create(
            phone="998900000001",
            first_name="Super",
            last_name="Admin",
            role="super_admin",
            organization=self.org
        )
        
        self.admin = User.objects.create(
            phone="998900000002",
            first_name="Test",
            last_name="Admin",
            role="admin",
            organization=self.org
        )
        
        # Create accounts
        self.main_account = Account.objects.create(
            organization=self.org,
            name="Asosiy Kassa",
            account_type="cash",
            balance=Decimal("1000000.00")
        )
        
        self.admin_account = Account.objects.create(
            organization=self.org,
            name="Admin Kassa - Test Admin",
            account_type="cash",
            balance=Decimal("500000.00")
        )
        
        # Create categories
        self.income_category = TransactionCategory.objects.create(
            organization=self.org,
            name="Kurs to'lovi",
            transaction_type="income"
        )
        
        self.expense_category = TransactionCategory.objects.create(
            organization=self.org,
            name="Xodimlar oyligi",
            transaction_type="expense"
        )
    
    def test_dashboard_income_calculation_excludes_transfers(self):
        """Test that dashboard income calculation excludes transfer transactions"""
        today = date.today()
        
        # Create real income transaction (should be counted)
        Transaction.objects.create(
            organization=self.org,
            account=self.main_account,
            category=self.income_category,
            amount=Decimal("100000.00"),
            transaction_type="income",
            description="Student payment",
            status="confirmed",
            created_by=self.admin
        )
        
        # Create transfer transaction (should NOT be counted as income)
        Transaction.objects.create(
            organization=self.org,
            account=self.main_account,
            amount=Decimal("50000.00"),
            transaction_type="transfer",
            description="Transfer from admin account",
            status="confirmed",
            created_by=self.admin
        )
        
        # Create salary expense (should be counted as expense)
        Transaction.objects.create(
            organization=self.org,
            account=self.main_account,
            category=self.expense_category,
            amount=Decimal("75000.00"),
            transaction_type="salary",
            description="Teacher salary",
            status="confirmed",
            created_by=self.admin
        )
        
        # Mock request object for dashboard function
        class MockRequest:
            def __init__(self, user, organization):
                self.user = user
                self.organization = organization
                self.GET = {}
        
        request = MockRequest(self.super_admin, self.org)
        
        # Test the dashboard function
        context = super_admin_dashboard(request)
        
        # Verify calculations
        self.assertEqual(context['today_income'], Decimal("100000.00"), 
                        "Only real income should be counted, transfers should be excluded")
        self.assertEqual(context['today_expense'], Decimal("75000.00"), 
                        "Salary should be counted as expense")
        self.assertEqual(context['net_profit'], Decimal("100000.00") - Decimal("75000.00"),
                        "Net profit should exclude transfers")
        
        # Verify account balances are included
        self.assertEqual(context['main_cash_balance'], Decimal("1000000.00"),
                        "Main cash balance should be included")
        self.assertEqual(context['admin_cash_balance'], Decimal("500000.00"),
                        "Admin cash balance should be included")
        
        print("✅ Dashboard calculation test passed!")
        print(f"   Today's income: {context['today_income']} UZS (excludes transfers)")
        print(f"   Today's expense: {context['today_expense']} UZS")
        print(f"   Net profit: {context['net_profit']} UZS")
        print(f"   Main cash balance: {context['main_cash_balance']} UZS")
        print(f"   Admin cash balance: {context['admin_cash_balance']} UZS")
    
    def test_dashboard_monthly_calculation(self):
        """Test monthly period calculation with proper income/expense distinction"""
        # Create transactions for different dates
        base_date = date.today() - timedelta(days=15)
        
        # Real income in the period
        Transaction.objects.create(
            organization=self.org,
            account=self.main_account,
            category=self.income_category,
            amount=Decimal("200000.00"),
            transaction_type="income",
            description="Monthly student payments",
            status="confirmed",
            created_at=base_date,
            created_by=self.admin
        )
        
        # Transfer (should not be counted)
        Transaction.objects.create(
            organization=self.org,
            account=self.main_account,
            amount=Decimal("100000.00"),
            transaction_type="transfer",
            description="Internal transfer",
            status="confirmed",
            created_at=base_date + timedelta(days=2),
            created_by=self.admin
        )
        
        # Expense in the period
        Transaction.objects.create(
            organization=self.org,
            account=self.main_account,
            category=self.expense_category,
            amount=Decimal("150000.00"),
            transaction_type="expense",
            description="Monthly expenses",
            status="confirmed",
            created_at=base_date + timedelta(days=5),
            created_by=self.admin
        )
        
        # Mock request with monthly period
        class MockRequest:
            def __init__(self, user, organization):
                self.user = user
                self.organization = organization
                self.GET = {'period': 'monthly'}
        
        request = MockRequest(self.super_admin, self.org)
        
        # Test the dashboard function
        context = super_admin_dashboard(request)
        
        # Verify monthly calculations exclude transfers
        self.assertEqual(context['period_income'], Decimal("200000.00"),
                        "Monthly income should only include real income, not transfers")
        self.assertEqual(context['period_expense'], Decimal("150000.00"),
                        "Monthly expense should include real expenses")
        self.assertEqual(context['net_profit'], Decimal("200000.00") - Decimal("150000.00"),
                        "Monthly net profit should exclude transfers")
        
        print("✅ Monthly dashboard calculation test passed!")
        print(f"   Period income: {context['period_income']} UZS")
        print(f"   Period expense: {context['period_expense']} UZS")
        print(f"   Net profit: {context['net_profit']} UZS")

if __name__ == "__main__":
    import django
    django.setup()
    import unittest
    unittest.main()