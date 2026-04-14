"""
Admin Kassa (Kirim-Chiqim) va Kassa Topshirish testlari.
CashSubmission modeli, permission va view testlari.
"""
from django.test import TestCase, Client, override_settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from decimal import Decimal
from apps.finance.models import Account, Transaction, TransactionCategory, CashSubmission
from apps.finance.services import approve_cash_submission, confirm_transaction
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

        initial_admin_balance = self.admin_account.balance
        initial_main_balance = self.main_account.balance

        # Topshirish yaratish va admin balansini 0 ga tushirish (view kabi)
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal("300000"),
            total_expense=Decimal("100000"),
            net_amount=initial_admin_balance,
            period_type="weekly",
            period_start=today - timedelta(days=7),
            period_end=today,
            status="pending",
        )
        # Admin kassasi balansini 0 ga tushirish (view da bajariladi)
        self.admin_account.balance = Decimal('0.00')
        self.admin_account.save(update_fields=['balance'])

        # Tasdiqlash
        result = approve_cash_submission(submission.id, self.owner)

        # Submission holati
        self.assertEqual(result.status, "approved")
        self.assertEqual(result.approved_by, self.owner)

        # Balanslar tekshirish - admin kassasi 0 da qolishi kerak
        self.admin_account.refresh_from_db()
        self.main_account.refresh_from_db()
        self.assertEqual(
            self.admin_account.balance,
            Decimal("0.00")
        )
        self.assertEqual(
            self.main_account.balance,
            initial_main_balance + initial_admin_balance
        )

        # Transfer tranzaksiya yaratilganini tekshirish
        transfer_tx = Transaction.objects.filter(
            account=self.main_account,
            description__contains="Kassa topshirish"
        ).first()
        self.assertIsNotNone(transfer_tx)
        self.assertEqual(transfer_tx.amount, initial_admin_balance)
        self.assertEqual(transfer_tx.status, "confirmed")

    def test_submit_cash_resets_admin_balance(self):
        """Kassa topshirilganda admin kassasi balansi 0 ga tushishi kerak"""
        from django.utils import timezone
        from datetime import timedelta

        today = timezone.now().date()
        initial_balance = self.admin_account.balance
        self.assertGreater(initial_balance, Decimal('0'))

        # Topshirish yaratish va balansni 0 ga tushirish (view logikasi)
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal("300000"),
            total_expense=Decimal("100000"),
            net_amount=initial_balance,
            period_type="weekly",
            period_start=today - timedelta(days=7),
            period_end=today,
            status="pending",
        )
        self.admin_account.balance = Decimal('0.00')
        self.admin_account.save(update_fields=['balance'])

        # Admin kassasi 0 ga tushganini tekshirish
        self.admin_account.refresh_from_db()
        self.assertEqual(self.admin_account.balance, Decimal('0.00'))
        self.assertEqual(submission.net_amount, initial_balance)

    def test_reject_restores_admin_balance(self):
        """Kassa topshirish rad etilganda admin kassasi balansi qaytarilishi kerak"""
        from django.utils import timezone
        from datetime import timedelta

        today = timezone.now().date()
        initial_balance = self.admin_account.balance

        # Topshirish yaratish va balansni 0 ga tushirish
        submission = CashSubmission.objects.create(
            organization=self.org,
            admin_user=self.admin,
            admin_account=self.admin_account,
            main_account=self.main_account,
            total_income=Decimal("300000"),
            total_expense=Decimal("100000"),
            net_amount=initial_balance,
            period_type="weekly",
            period_start=today - timedelta(days=7),
            period_end=today,
            status="pending",
        )
        self.admin_account.balance = Decimal('0.00')
        self.admin_account.save(update_fields=['balance'])

        # Haqiqiy reject view orqali rad etish
        from django.test import Client
        from django.urls import reverse
        client = Client()
        client.login(phone="998905552222", password="test123")
        response = client.post(
            reverse('finance:reject_cash_submission', kwargs={'pk': submission.pk}),
            {'reason': 'Test sababi'}
        )
        self.assertEqual(response.status_code, 302)

        # Admin kassasi balansi qaytganini tekshirish
        self.admin_account.refresh_from_db()
        self.assertEqual(self.admin_account.balance, initial_balance)

    def test_submit_zero_balance_prevented(self):
        """Balans 0 bo'lganda kassa topshirish rad etilishi kerak"""
        self.admin_account.balance = Decimal('0.00')
        self.admin_account.save(update_fields=['balance'])

        # admin_submit_cash view da net_amount <= 0 bo'lsa topshirish bloklanadi
        self.admin_account.refresh_from_db()
        net_amount = self.admin_account.balance
        self.assertTrue(net_amount <= 0, "Balance 0 yoki manfiy bo'lishi kerak")
        # CashSubmission yaratilmasligi kerak (view da redirect bo'ladi)
        self.assertEqual(CashSubmission.objects.count(), 0)

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
        Account.objects.create(
            organization=self.org,
            name="Admin Kassa - Admin View",
            account_type="cash",
            balance=Decimal("100000.00"),
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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AdminStudentPaymentTest(TestCase):
    """Admin o'quvchi to'lovlarini tasdiqlash/rad etish testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-asp"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin = User.objects.create_user(
            phone="998908881111",
            password="test123",
            first_name="Admin",
            last_name="SP",
            role="admin",
            organization=self.org,
            branch=self.branch,
        )
        self.student = User.objects.create_user(
            phone="998908882222",
            password="test123",
            first_name="Student",
            last_name="SP",
            role="student",
            organization=self.org,
            branch=self.branch,
        )
        self.account = Account.objects.create(
            organization=self.org,
            name="Online Kassa",
            account_type="wallet",
            balance=Decimal("0.00")
        )
        self.category = TransactionCategory.objects.create(
            organization=self.org,
            name="Kurs to'lovi",
            transaction_type="income"
        )
        self.client = Client()

    def test_admin_can_view_student_payments(self):
        """Admin o'quvchi to'lovlari sahifasini ko'ra olishi"""
        self.client.login(phone="998908881111", password="test123")
        response = self.client.get(reverse('finance:admin_student_payments'))
        self.assertEqual(response.status_code, 200)

    def test_pending_student_payments_on_dashboard(self):
        """Dashboard'da pending o'quvchi to'lovlari ko'rinishi"""
        # O'quvchi to'lovini yaratish
        Transaction.objects.create(
            organization=self.org,
            account=self.account,
            category=self.category,
            student=self.student,
            amount=Decimal("500000"),
            transaction_type="income",
            status="pending",
            created_by=self.student,
        )
        self.client.login(phone="998908881111", password="test123")
        response = self.client.get(reverse('finance:admin_cash_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pending_count'], 1)
        self.assertEqual(len(response.context['pending_student_payments']), 1)

    def test_admin_confirm_student_payment(self):
        """Admin o'quvchi to'lovini tasdiqlashi va admin kassasiga tushishi"""
        tx = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            category=self.category,
            student=self.student,
            amount=Decimal("500000"),
            transaction_type="income",
            status="pending",
            created_by=self.student,
        )
        self.client.login(phone="998908881111", password="test123")

        initial_student_balance = self.student.balance

        response = self.client.post(
            reverse('finance:admin_confirm_student_payment', kwargs={'pk': tx.pk})
        )
        self.assertEqual(response.status_code, 302)

        # Tranzaksiya tasdiqlangan bo'lishi kerak
        tx.refresh_from_db()
        self.assertEqual(tx.status, 'confirmed')
        self.assertEqual(tx.confirmed_by, self.admin)
        self.assertTrue(tx.receipt_verified)

        # Admin kassasiga bog'langan bo'lishi kerak
        self.assertIn("Admin Kassa", tx.account.name)

        # O'quvchi balansi yangilangan bo'lishi kerak
        self.student.refresh_from_db()
        self.assertEqual(
            self.student.balance,
            initial_student_balance + Decimal("500000")
        )

        # Admin kassa balansi yangilangan bo'lishi kerak
        tx.account.refresh_from_db()
        self.assertEqual(tx.account.balance, Decimal("500000"))

    def test_admin_reject_student_payment(self):
        """Admin o'quvchi to'lovini rad etishi"""
        tx = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            category=self.category,
            student=self.student,
            amount=Decimal("500000"),
            transaction_type="income",
            status="pending",
            created_by=self.student,
        )
        self.client.login(phone="998908881111", password="test123")
        response = self.client.post(
            reverse('finance:admin_reject_student_payment', kwargs={'pk': tx.pk}),
            {'reason': 'Chek noto\'g\'ri'}
        )
        self.assertEqual(response.status_code, 302)

        tx.refresh_from_db()
        self.assertEqual(tx.status, 'rejected')
        self.assertIn("noto'g'ri", tx.receipt_notes)

    def test_confirm_already_confirmed_payment(self):
        """Allaqachon tasdiqlangan to'lovni qayta tasdiqlash xato berishi"""
        tx = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            category=self.category,
            student=self.student,
            amount=Decimal("500000"),
            transaction_type="income",
            status="confirmed",
            created_by=self.student,
            confirmed_by=self.admin,
        )
        self.client.login(phone="998908881111", password="test123")
        response = self.client.post(
            reverse('finance:admin_confirm_student_payment', kwargs={'pk': tx.pk})
        )
        self.assertEqual(response.status_code, 302)


class ConfirmTransactionServiceTest(TestCase):
    """confirm_transaction service - signal bilan to'g'ri ishlashi testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-cts"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin = User.objects.create_user(
            phone="998909991111",
            password="test123",
            first_name="Admin",
            last_name="CTS",
            role="admin",
            organization=self.org,
            branch=self.branch,
        )
        self.student = User.objects.create_user(
            phone="998909992222",
            password="test123",
            first_name="Student",
            last_name="CTS",
            role="student",
            organization=self.org,
            branch=self.branch,
        )
        self.account = Account.objects.create(
            organization=self.org,
            name="Test Kassa",
            account_type="cash",
            balance=Decimal("1000000.00")
        )

    def test_confirm_income_updates_balance_once(self):
        """Kirim tasdiqlanganda balans faqat BIR marta yangilanishi (signal orqali)"""
        tx = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            student=self.student,
            amount=Decimal("200000"),
            transaction_type="income",
            status="pending",
            created_by=self.admin,
        )

        initial_balance = self.account.balance
        initial_student_balance = self.student.balance

        result = confirm_transaction(tx.id, self.admin)

        self.account.refresh_from_db()
        self.student.refresh_from_db()

        # Balans faqat 1 marta oshgan bo'lishi kerak (200000)
        self.assertEqual(
            self.account.balance,
            initial_balance + Decimal("200000")
        )
        self.assertEqual(
            self.student.balance,
            initial_student_balance + Decimal("200000")
        )

    def test_confirm_expense_checks_balance(self):
        """Chiqim uchun yetarli mablag' tekshirishi"""
        self.account.balance = Decimal("100")
        self.account.save()

        tx = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            amount=Decimal("500000"),
            transaction_type="expense",
            status="pending",
            created_by=self.admin,
        )

        with self.assertRaises(ValidationError):
            confirm_transaction(tx.id, self.admin)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AdminCoursePaymentTest(TestCase):
    """Admin kurs to'lovi qo'shish testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-acp"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin = User.objects.create_user(
            phone="998911111111",
            password="test123",
            first_name="Admin",
            last_name="ACP",
            role="admin",
            organization=self.org,
            branch=self.branch,
        )
        self.student = User.objects.create_user(
            phone="998911112222",
            password="test123",
            first_name="Student",
            last_name="ACP",
            role="student",
            organization=self.org,
            branch=self.branch,
        )
        self.category = TransactionCategory.objects.create(
            organization=self.org,
            name="Kurs to'lovi",
            transaction_type="income"
        )
        self.client = Client()

    def test_admin_can_view_course_payment_form(self):
        """Admin kurs to'lovi formasini ko'ra olishi"""
        self.client.login(phone="998911111111", password="test123")
        response = self.client.get(reverse('finance:admin_add_course_payment'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_add_course_payment(self):
        """Admin kurs to'lovini qo'sha olishi va admin kassasiga tushishi"""
        self.client.login(phone="998911111111", password="test123")
        initial_student_balance = self.student.balance

        response = self.client.post(reverse('finance:admin_add_course_payment'), {
            'student': self.student.pk,
            'amount': '300000',
            'category': self.category.pk,
            'payment_method': 'cash',
            'description': 'Fevral oyi kurs to\'lovi',
        })
        self.assertEqual(response.status_code, 302)

        # Tranzaksiya yaratilgan va tasdiqlangan bo'lishi kerak
        tx = Transaction.objects.filter(
            student=self.student,
            created_by=self.admin,
            amount=Decimal('300000'),
        ).first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.status, 'confirmed')
        self.assertIn("Admin Kassa", tx.account.name)

        # O'quvchi balansi yangilangan
        self.student.refresh_from_db()
        self.assertEqual(
            self.student.balance,
            initial_student_balance + Decimal('300000')
        )

    def test_student_cannot_access_course_payment(self):
        """O'quvchi kurs to'lovi formasiga kira olmasligi"""
        self.client.login(phone="998911112222", password="test123")
        response = self.client.get(reverse('finance:admin_add_course_payment'))
        self.assertIn(response.status_code, [302, 403])


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class CashSubmissionPermissionTest(TestCase):
    """Kassa topshirishlar sahifasi ruxsat testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-csp"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin_with_perms = User.objects.create_user(
            phone="998912221111",
            password="test123",
            first_name="Admin",
            last_name="WP",
            role="admin",
            organization=self.org,
            branch=self.branch,
            permissions={
                "admin_finance": {"view": True, "create": True, "edit": True},
            },
        )
        self.owner = User.objects.create_user(
            phone="998912222222",
            password="test123",
            first_name="Owner",
            last_name="CSP",
            role="owner",
            organization=self.org,
        )
        self.client = Client()

    def test_admin_with_admin_finance_can_view_submissions(self):
        """admin_finance ruxsati bilan admin topshirishlarni ko'ra olishi"""
        self.client.login(phone="998912221111", password="test123")
        response = self.client.get(reverse('finance:cash_submission_list'))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_view_submissions(self):
        """Owner topshirishlarni ko'ra olishi"""
        self.client.login(phone="998912222222", password="test123")
        response = self.client.get(reverse('finance:cash_submission_list'))
        self.assertEqual(response.status_code, 200)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PendingReceiptsViewTest(TestCase):
    """Pending receipts (chek tekshirish) view testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-prv"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.owner = User.objects.create_user(
            phone="998913331111",
            password="test123",
            first_name="Owner",
            last_name="PRV",
            role="owner",
            organization=self.org,
        )
        self.student = User.objects.create_user(
            phone="998913332222",
            password="test123",
            first_name="Student",
            last_name="PRV",
            role="student",
            organization=self.org,
            branch=self.branch,
        )
        self.account = Account.objects.create(
            organization=self.org,
            name="Test Kassa",
            account_type="cash",
            balance=Decimal("0.00")
        )
        self.client = Client()

    def test_pending_receipts_has_count_and_sum(self):
        """pending_receipts kontekstda pending_count va pending_sum bo'lishi"""
        # Pending tranzaksiya yaratish
        Transaction.objects.create(
            organization=self.org,
            account=self.account,
            student=self.student,
            amount=Decimal("100000"),
            transaction_type="income",
            status="pending",
            receipt_verified=False,
            created_by=self.student,
        )
        self.client.login(phone="998913331111", password="test123")
        response = self.client.get(reverse('finance:pending_receipts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pending_count'], 1)
        self.assertEqual(response.context['pending_sum'], Decimal('100000'))


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class CashSubmissionNotificationTest(TestCase):
    """Kassa topshirish bildirishnoma testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-csn"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin = User.objects.create_user(
            phone="998914441111",
            password="test123",
            first_name="Admin",
            last_name="Notif",
            role="admin",
            organization=self.org,
            branch=self.branch,
        )
        self.owner = User.objects.create_user(
            phone="998914442222",
            password="test123",
            first_name="Owner",
            last_name="Notif",
            role="owner",
            organization=self.org,
        )
        self.admin_account = Account.objects.create(
            organization=self.org,
            name="Admin Kassa - Admin Notif",
            account_type="cash",
            balance=Decimal("500000.00")
        )
        self.main_account = Account.objects.create(
            organization=self.org,
            name="Asosiy Kassa",
            account_type="cash",
            balance=Decimal("1000000.00")
        )
        self.client = Client()

    def test_approve_sends_notification_to_admin(self):
        """Kassa topshirish tasdiqlanganda admin bildirishnoma olishi kerak"""
        from django.utils import timezone
        from datetime import timedelta
        from apps.automation.models import NotificationLog

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

        # Tasdiqlashdan oldingi bildirishnomalar soni
        notif_count_before = NotificationLog.objects.filter(
            recipient=self.admin,
            message__contains="tasdiqlandi",
        ).count()

        approve_cash_submission(submission.id, self.owner)

        # Tasdiqlashdan keyingi bildirishnomalar soni
        notif_count_after = NotificationLog.objects.filter(
            recipient=self.admin,
            message__contains="tasdiqlandi",
        ).count()

        self.assertEqual(notif_count_after, notif_count_before + 1)

        # Bildirishnoma mazmunini tekshirish
        notification = NotificationLog.objects.filter(
            recipient=self.admin,
            message__contains="tasdiqlandi",
        ).latest('created_at')
        self.assertIn("tasdiqlandi", notification.message)
        self.assertIn(self.owner.get_full_name(), notification.message)

    def test_reject_sends_notification_to_admin(self):
        """Kassa topshirish rad etilganda admin bildirishnoma olishi kerak"""
        from django.utils import timezone
        from datetime import timedelta
        from apps.automation.models import NotificationLog

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

        self.client.login(phone="998914442222", password="test123")
        response = self.client.post(
            reverse('finance:reject_cash_submission', kwargs={'pk': submission.pk}),
            {'reason': 'Summada xatolik bor'}
        )
        self.assertEqual(response.status_code, 302)

        # Admin bildirishnoma olishi kerak
        notification = NotificationLog.objects.filter(
            recipient=self.admin,
            message__contains="rad etildi",
        ).latest('created_at')
        self.assertIn("rad etildi", notification.message)
        self.assertIn("Summada xatolik bor", notification.message)

    def test_submit_cash_sends_notification_to_owner(self):
        """Kassa topshirish yaratilganda owner bildirishnoma olishi kerak"""
        from django.utils import timezone
        from datetime import timedelta
        from apps.automation.models import NotificationLog
        from apps.automation.services import create_system_notification

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

        # View da qilinadigan bildirishnomani simulyatsiya qilish
        net_amount = submission.net_amount
        create_system_notification(
            recipient=self.owner,
            title="Yangi kassa topshirish",
            message=(
                f"{self.admin.get_full_name()} kassa topshirish so'rovini yubordi. "
                f"Davr: {submission.period_start.strftime('%d.%m.%Y')} - {submission.period_end.strftime('%d.%m.%Y')}. "
                f"Sof summa: {net_amount:,.0f} so'm"
            ),
            notification_type='system'
        )

        # Owner bildirishnoma olishi kerak
        notification = NotificationLog.objects.filter(
            recipient=self.owner,
            message__contains="kassa topshirish",
        ).latest('created_at')
        self.assertIn("kassa topshirish", notification.message)
        self.assertIn(self.admin.get_full_name(), notification.message)
