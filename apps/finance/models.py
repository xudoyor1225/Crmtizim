from django.db import models
from apps.core.models import TenantAwareModel
from apps.users.models import User
from apps.core.validators import validate_receipt_file, FileSizeValidator

# Import additional models from submodules
from apps.finance.payroll import StaffKPI, PayrollRecord, StaffAttendance
from apps.finance.inventory import AssetCategory, Asset, SupplyCategory, Supply, SupplyTransaction


class Account(TenantAwareModel):
    """
    Hisob raqamlar / Kassalar.
    M: 'Asosiy Kassa (Naqd)', 'Click Hamyon', 'Bank Hisob raqam'.
    """
    TYPE_CHOICES = (
        ('cash', 'Naqd pul'),
        ('bank', 'Bank hisobi'),
        ('card', 'Korporativ karta'),
        ('wallet', 'Elektron hamyon'),
    )

    name = models.CharField(max_length=100, verbose_name="Kassa nomi")
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='cash', verbose_name="Turi")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Joriy Balans")

    def __str__(self):
        return f"{self.name} ({self.balance:,.0f})"

    class Meta:
        db_table = 'finance_accounts'
        verbose_name = "Kassa / Hisob"
        verbose_name_plural = "Kassalar"


class TransactionCategory(TenantAwareModel):
    """
    Kirim va Chiqim turlari (Statistika uchun).
    M: 'Kurs to\'lovi', 'Arenda', 'Xodimlar oyligi', 'Marketing'.
    """
    TYPE_CHOICES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )

    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Turi")

    def __str__(self):
        return f"{self.name} ({self.get_transaction_type_display()})"

    class Meta:
        db_table = 'finance_categories'
        verbose_name = "Tranzaksiya Kategoriyasi"
        verbose_name_plural = "Tranzaksiya Kategoriyalari"


class Transaction(TenantAwareModel):
    """
    ENG MUHIM JADVAL.
    Har bir pul harakati shu yerda saqlanadi.
    """
    TYPE_CHOICES = (
        ('income', 'Kirim (To\'lov)'),
        ('expense', 'Chiqim (Xarajat)'),
        ('transfer', 'O\'tkazma'),
        ('salary', 'Oylik to\'lov'),
        ('refund', 'Pul qaytarish'),
    )

    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),  # Kassir kiritdi, hali tasdiqlanmadi
        ('confirmed', 'Tasdiqlandi'),  # Direktor tasdiqladi (Balans o'zgaradi)
        ('rejected', 'Rad etildi'),
    )

    # 1. Pul qayerga tushdi/chiqdi?
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactions', verbose_name="Kassa")
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True, verbose_name="Kategoriya")

    # 2. Kim bilan bog'liq?
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments',
                                limit_choices_to={'role': 'student'}, verbose_name="O'quvchi")
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='salaries',
                              limit_choices_to={'role__in': ['teacher', 'staff', 'admin']}, verbose_name="Xodim")

    # 3. Summa va Tafsilotlar
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Summa")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='income', verbose_name="Turi")
    description = models.TextField(blank=True, verbose_name="Izoh")
    
    # To'lov usuli
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Naqd pul'),
        ('card', 'Plastik karta'),
        ('transfer', 'Bank o\'tkazmasi'),
        ('online', 'Online to\'lov'),
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', 
                                      verbose_name="To'lov usuli")
    
    # Chek/Kvitansiya (rasm yoki PDF)
    receipt_image = models.ImageField(
        upload_to='receipts/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Chek rasmi",
        validators=[FileSizeValidator(max_size_mb=5)]
    )
    receipt_file = models.FileField(
        upload_to='receipts/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Chek fayli (PDF)",
        validators=[validate_receipt_file, FileSizeValidator(max_size_mb=5)]
    )

    # Chekni tasdiqlash (plastik to'lovlari uchun)
    receipt_verified = models.BooleanField(default=False, verbose_name="Chek tasdiqlandi")
    receipt_verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                            related_name='verified_receipts', verbose_name="Chekni tasdiqladi")
    receipt_verified_at = models.DateTimeField(null=True, blank=True, verbose_name="Tasdiqlash vaqti")
    receipt_notes = models.TextField(blank=True, verbose_name="Chek izohi")

    # 4. XAVFSIZLIK (Audit)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_transactions',
                                   verbose_name="Kiritdi")
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='confirmed_transactions', verbose_name="Tasdiqladi")
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount:,.0f}"

    class Meta:
        db_table = 'finance_transactions'
        ordering = ['-created_at']
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar"