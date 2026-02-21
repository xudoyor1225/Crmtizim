"""
Admin Kassa (Kirim-Chiqim) va Kassa Topshirish testlari.
CashSubmission modeli, permission va view testlari.
"""
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.urls import reverse
from decimal import Decimal
from apps.finance.models import Account, Transaction, TransactionCategory, CashSubmission
from apps.finance.services import approve_cash_submission
from apps.users.models import User
from apps.organizations.models import Organization, Branch
from apps.core.permissions import check_permission


class CashSubmissionModelTest(TestCase):
    """CashSubmission modeli testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-cs"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin = User.objects.create_user(
            phone="998905551111",
            password="test123",
            first_name="Admin",
            last_name="Test",
            role="admin",
            organization=self.org,
            branch=self.branch
        )
        self.owner = User.objects.create_user(
            phone="998905552222",
            password="test123",
            first_name="Owner",
            last_name="Test",
            role="owner",
            organization=self.org,
        )
        self.admin_account = Account.objects.create(
            organization=self.org,
            name="Admin Kassa - Admin Test",
            account_type="cash",
            balance=Decimal("500000.00")
        )
        self.main_account = Account.objects.create(
            organization=self.org,
            name="Asosiy Kassa",
            account_type="cash",
            balance=Decimal("1000000.00")
        )

    def test_create_cash_submission(self):
        """CashSubmission yaratish testi"""
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal("300000"),
            total_expense=Decimal("100000"),
            net_amount=Decimal("200000"),
            period_type="weekly",
            period_start=today - timedelta(days=7),
            period_end=today,
            status="pending",
        )
        self.assertEqual(submission.status, "pending")
        self.assertEqual(submission.net_amount, Decimal("200000"))
        self.assertEqual(submission.admin_user, self.admin)

    def test_approve_cash_submission_service(self):
        """approve_cash_submission service testi - pul asosiy kassaga o'tishi"""
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal("300000"),
            total_expense=Decimal("100000"),
            net_amount=Decimal("200000"),
            period_type="weekly",
            period_start=today - timedelta(days=7),
            period_end=today,
            status="pending",
        )

        initial_admin_balance = self.admin_account.balance
        initial_main_balance = self.main_account.balance

        # Tasdiqlash
        result = approve_cash_submission(submission.id, self.owner)

        # Submission holati
        self.assertEqual(result.status, "approved")
        self.assertEqual(result.approved_by, self.owner)

        # Balanslar tekshirish
        self.admin_account.refresh_from_db()
        self.main_account.refresh_from_db()
        self.assertEqual(
            self.admin_account.balance,
            initial_admin_balance - Decimal("200000")
        )
        self.assertEqual(
            self.main_account.balance,
            initial_main_balance + Decimal("200000")
        )

        # Transfer tranzaksiya yaratilganini tekshirish
        transfer_tx = Transaction.objects.filter(
            account=self.main_account,
            description__contains="Kassa topshirish"
        ).first()
        self.assertIsNotNone(transfer_tx)
        self.assertEqual(transfer_tx.amount, Decimal("200000"))
        self.assertEqual(transfer_tx.status, "confirmed")

    def test_approve_already_approved_submission(self):
        """Allaqachon tasdiqlangan topshirishni qayta tasdiqlash xatosi"""
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal("100000"),
            total_expense=Decimal("0"),
            net_amount=Decimal("100000"),
            period_type="monthly",
            period_start=today - timedelta(days=30),
            period_end=today,
            status="approved",
        )

        with self.assertRaises(ValidationError):
            approve_cash_submission(submission.id, self.owner)


class AdminFinancePermissionTest(TestCase):
    """Admin finance ruxsatlari testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-afp"
        )

    def test_admin_has_admin_finance_permission(self):
        """Admin admin_finance moduli uchun ruxsatga ega"""
        admin = User.objects.create_user(
            phone="998906661111",
            password="test123",
            role="admin",
            organization=self.org,
            permissions={
                "admin_finance": {"view": True, "create": True}
            },
        )
        self.assertTrue(check_permission(admin, 'admin_finance', 'view'))
        self.assertTrue(check_permission(admin, 'admin_finance', 'create'))

    def test_admin_without_full_finance_sees_admin_finance(self):
        """Finance ruxsati bo'lmagan admin faqat admin_finance ko'rishi kerak"""
        admin = User.objects.create_user(
            phone="998906662222",
            password="test123",
            role="admin",
            organization=self.org,
            permissions={
                "admin_finance": {"view": True, "create": True},
                # finance moduliga ruxsat yo'q
            },
        )
        self.assertTrue(check_permission(admin, 'admin_finance', 'view'))
        self.assertFalse(check_permission(admin, 'finance', 'view'))

    def test_super_admin_has_admin_finance_permission(self):
        """Super admin admin_finance moduli uchun ruxsatga ega"""
        super_admin = User.objects.create_user(
            phone="998906663333",
            password="test123",
            role="super_admin",
            organization=None,
        )
        self.assertTrue(check_permission(super_admin, 'admin_finance', 'view'))
        self.assertTrue(check_permission(super_admin, 'admin_finance', 'create'))

    def test_staff_without_permission_cannot_access_admin_finance(self):
        """Ruxsatsiz xodim admin_finance ga kira olmasligi kerak"""
        staff = User.objects.create_user(
            phone="998906664444",
            password="test123",
            role="staff",
            organization=self.org,
            permissions={},
        )
        self.assertFalse(check_permission(staff, 'admin_finance', 'view'))


class AdminCashViewTest(TestCase):
    """Admin kassa viewlari testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-acv"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin = User.objects.create_user(
            phone="998907771111",
            password="test123",
            first_name="Admin",
            last_name="View",
            role="admin",
            organization=self.org,
            branch=self.branch,
        )
        self.owner = User.objects.create_user(
            phone="998907772222",
            password="test123",
            first_name="Owner",
            last_name="View",
            role="owner",
            organization=self.org,
        )
        self.main_account = Account.objects.create(
            organization=self.org,
            name="Asosiy Kassa",
            account_type="cash",
            balance=Decimal("1000000.00")
        )
        self.category = TransactionCategory.objects.create(
            organization=self.org,
            name="Boshqa kirim",
            transaction_type="income"
        )
        self.client = Client()

    def test_admin_add_income(self):
        """Admin kirim qo'shishi"""
        self.client.login(phone="998907771111", password="test123")
        response = self.client.post(reverse('finance:admin_add_income'), {
            'category': self.category.pk,
            'amount': '100000',
            'description': 'Test kirim',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(
            created_by=self.admin,
            amount=Decimal('100000'),
            transaction_type='income'
        ).exists())

    def test_admin_add_expense(self):
        """Admin chiqim qo'shishi"""
        expense_cat = TransactionCategory.objects.create(
            organization=self.org,
            name="Boshqa chiqim",
            transaction_type="expense"
        )
        self.client.login(phone="998907771111", password="test123")
        response = self.client.post(reverse('finance:admin_add_expense'), {
            'category': expense_cat.pk,
            'amount': '50000',
            'description': 'Test chiqim',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(
            created_by=self.admin,
            amount=Decimal('50000'),
            transaction_type='expense'
        ).exists())

    def test_student_cannot_access_admin_cash(self):
        """O'quvchi admin kassaga kira olmasligi kerak"""
        student = User.objects.create_user(
            phone="998907773333",
            password="test123",
            first_name="Student",
            last_name="Test",
            role="student",
            organization=self.org,
        )
        self.client.login(phone="998907773333", password="test123")
        response = self.client.post(reverse('finance:admin_add_income'), {
            'category': self.category.pk,
            'amount': '100000',
        })
        # Should redirect (permission denied redirects to dashboard)
        self.assertIn(response.status_code, [302, 403])
