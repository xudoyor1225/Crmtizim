"""
Finance moduli uchun testlar.
Transaction, Account, Balance avtomatik yangilanishi testlari.
"""
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.urls import reverse
from decimal import Decimal
import json
from apps.finance.models import Account, Transaction, TransactionCategory
from apps.users.models import User
from apps.organizations.models import Organization, Branch


class TransactionTestCase(TestCase):
    """Transaction modeli testlari"""

    def setUp(self):
        """Test uchun kerakli obyektlarni yaratish"""
        # Organization
        self.org = Organization.objects.create(
            name="Test O'quv Markazi",
            subdomain="test"
        )

        # Branch
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )

        # Admin
        self.admin = User.objects.create_user(
            phone="998901111111",
            password="test123",
            first_name="Admin",
            last_name="User",
            role="admin",
            organization=self.org,
            branch=self.branch
        )

        # Student
        self.student = User.objects.create_user(
            phone="998902222222",
            password="test123",
            first_name="Student",
            last_name="User",
            role="student",
            organization=self.org,
            branch=self.branch
        )

        # Account (Kassa)
        self.account = Account.objects.create(
            organization=self.org,
            name="Asosiy Kassa",
            account_type="cash",
            balance=Decimal("1000000.00")
        )

        # Category
        self.category = TransactionCategory.objects.create(
            organization=self.org,
            name="Kurs to'lovi",
            transaction_type="income"
        )

    def test_create_transaction(self):
        """Transaction yaratish testi"""
        transaction = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            category=self.category,
            student=self.student,
            amount=Decimal("500000.00"),
            transaction_type="income",
            status="pending",
            created_by=self.admin
        )

        self.assertEqual(transaction.amount, Decimal("500000.00"))
        self.assertEqual(transaction.status, "pending")

    def test_balance_update_on_confirmation(self):
        """Tasdiqlanganda balans yangilanishi testi"""
        initial_account_balance = self.account.balance
        initial_student_balance = self.student.balance

        transaction = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            category=self.category,
            student=self.student,
            amount=Decimal("500000.00"),
            transaction_type="income",
            status="pending",
            created_by=self.admin
        )

        # Pending da balans o'zgarmasligi kerak
        self.account.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(self.account.balance, initial_account_balance)
        self.assertEqual(self.student.balance, initial_student_balance)

        # Tasdiqlash
        transaction.status = "confirmed"
        transaction.confirmed_by = self.admin
        transaction.save()

        # Balans o'zgargan bo'lishi kerak
        self.account.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(
            self.account.balance,
            initial_account_balance + Decimal("500000.00")
        )
        self.assertEqual(
            self.student.balance,
            initial_student_balance + Decimal("500000.00")
        )

    def test_prevent_edit_confirmed_transaction(self):
        """Tasdiqlangan tranzaksiyani o'zgartirishni oldini olish"""
        transaction = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            category=self.category,
            student=self.student,
            amount=Decimal("500000.00"),
            transaction_type="income",
            status="confirmed",
            created_by=self.admin,
            confirmed_by=self.admin
        )

        # Amount o'zgartirishga urinish
        transaction.amount = Decimal("600000.00")

        with self.assertRaises(ValidationError):
            transaction.save()

    def test_expense_decreases_balance(self):
        """Chiqim kassadan pul ayirishi"""
        initial_balance = self.account.balance

        transaction = Transaction.objects.create(
            organization=self.org,
            account=self.account,
            amount=Decimal("100000.00"),
            transaction_type="expense",
            status="confirmed",
            description="Arenda to'lovi",
            created_by=self.admin,
            confirmed_by=self.admin
        )

        self.account.refresh_from_db()
        self.assertEqual(
            self.account.balance,
            initial_balance - Decimal("100000.00")
        )


class AccountTestCase(TestCase):
    """Account modeli testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test"
        )

    def test_create_account(self):
        """Kassa yaratish"""
        account = Account.objects.create(
            organization=self.org,
            name="Naqd Kassa",
            account_type="cash",
            balance=Decimal("0.00")
        )

        self.assertEqual(account.name, "Naqd Kassa")
        self.assertEqual(account.balance, Decimal("0.00"))

    def test_account_str_method(self):
        """__str__ method testi"""
        account = Account.objects.create(
            organization=self.org,
            name="Click",
            balance=Decimal("1500000.00")
        )

        expected = "Click (1,500,000)"
        self.assertEqual(str(account), expected)


class QuickPaymentTestCase(TestCase):
    """Quick Payment AJAX view testlari"""

    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Markaz",
            subdomain="test-qp"
        )
        self.branch = Branch.objects.create(
            organization=self.org,
            name="Test Filial"
        )
        self.admin = User.objects.create_user(
            phone="998903331111",
            password="test123",
            first_name="Admin",
            last_name="QP",
            role="admin",
            organization=self.org,
            branch=self.branch
        )
        self.student = User.objects.create_user(
            phone="998903332222",
            password="test123",
            first_name="Student",
            last_name="QP",
            role="student",
            organization=self.org,
            branch=self.branch
        )
        self.account = Account.objects.create(
            organization=self.org,
            name="Naqd Kassa",
            account_type="cash",
            balance=Decimal("0.00")
        )
        self.client = Client()
        self.client.login(phone="998903331111", password="test123")

    def test_quick_payment_success(self):
        """Muvaffaqiyatli quick payment"""
        response = self.client.post(reverse('finance:quick_payment'), {
            'student_id': self.student.id,
            'amount': '500000',
            'payment_method': 'cash',
            'account_id': self.account.id,
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('transaction_id', data)
        # Tranzaksiya yaratilganini tekshirish
        self.assertTrue(Transaction.objects.filter(
            student=self.student, amount=Decimal('500000')
        ).exists())

    def test_quick_payment_missing_fields(self):
        """Maydonlar to'ldirilmaganida xatolik"""
        response = self.client.post(reverse('finance:quick_payment'), {
            'student_id': self.student.id,
            # amount va account_id yo'q
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_quick_payment_invalid_amount(self):
        """Noto'g'ri summa kiritilganida xatolik"""
        response = self.client.post(reverse('finance:quick_payment'), {
            'student_id': self.student.id,
            'amount': '-100',
            'payment_method': 'cash',
            'account_id': self.account.id,
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_quick_payment_get_not_allowed(self):
        """GET so'rovi rad etilishi kerak"""
        response = self.client.get(reverse('finance:quick_payment'))
        self.assertEqual(response.status_code, 405)
