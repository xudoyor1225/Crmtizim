from django import forms
from apps.users.models import User, ParentStudent


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Parol")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'role', 'branch', 'password', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ismi', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Familiyasi', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '998901234567', 'required': True}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


# ============================================
# O'QUVCHI FORMASI (Majburiy Ota-Ona bilan)
# ============================================
class StudentForm(forms.ModelForm):
    """O'quvchi qo'shish formasi - ota-ona va manzil majburiy"""
    
    # Parol
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '********'}),
        required=True, 
        label="Parol"
    )
    
    # MANZIL MA'LUMOTLARI (profile_data ichida saqlanadi)
    region = forms.CharField(
        max_length=100, 
        required=True,
        label="Viloyat",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Masalan: Toshkent shahri"})
    )
    district = forms.CharField(
        max_length=100, 
        required=True,
        label="Tuman/Shahar",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Masalan: Chilonzor tumani"})
    )
    address = forms.CharField(
        max_length=255, 
        required=True,
        label="Ko'cha, uy",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Masalan: Bunyodkor ko'chasi, 15-uy"})
    )
    
    # OTA-ONA MA'LUMOTLARI (Dinamik - template da boshqariladi)
    parent_first_name = forms.CharField(
        max_length=50, 
        required=False,
        label="Ota-ona ismi",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Ismi"})
    )
    parent_last_name = forms.CharField(
        max_length=50, 
        required=False,
        label="Ota-ona familiyasi",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Familiyasi"})
    )
    parent_phone = forms.CharField(
        max_length=20, 
        required=False,
        label="Ota-ona telefoni",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "998901234567"})
    )
    relation_type = forms.ChoiceField(
        choices=ParentStudent.RELATION_TYPES,
        required=False,
        label="Qarindoshligi",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'middle_name', 'phone', 
            'birth_date', 'branch', 'avatar'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ismi', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Familiyasi', 'required': True}),
            'middle_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Otasining ismi'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '998901234567', 'required': True}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
        }
        labels = {
            'first_name': 'Ismi',
            'last_name': 'Familiyasi',
            'middle_name': 'Otasining ismi',
            'phone': 'Telefon raqami',
            'birth_date': "Tug'ilgan sana",
            'branch': 'Filial',
            'avatar': 'Rasm',
        }

    def save(self, commit=True, organization=None):
        user = super().save(commit=False)
        user.role = 'student'
        user.set_password(self.cleaned_data['password'])
        
        # Manzil ma'lumotlarini profile_data ga saqlash
        user.profile_data = {
            'region': self.cleaned_data.get('region', ''),
            'district': self.cleaned_data.get('district', ''),
            'address': self.cleaned_data.get('address', ''),
        }
        
        if organization:
            user.organization = organization
            
        if commit:
            user.save()
        return user


# ============================================
# O'QITUVCHI FORMASI (NFC Card bilan)
# ============================================
class TeacherForm(forms.ModelForm):
    """O'qituvchi qo'shish formasi - NFC card va to'liq ma'lumotlar"""
    
    # Parol
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '********'}),
        required=True, 
        label="Parol"
    )
    
    # Qo'shimcha HR ma'lumotlari
    passport_series = forms.CharField(
        max_length=20, 
        required=False,
        label="Pasport seriyasi",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "AA1234567"})
    )
    
    # Manzil
    address = forms.CharField(
        max_length=255, 
        required=False,
        label="Manzil",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "To'liq manzil"})
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'middle_name', 'phone', 
            'birth_date', 'branch', 'avatar', 'nfc_card_id'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ismi', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Familiyasi', 'required': True}),
            'middle_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Otasining ismi'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '998901234567', 'required': True}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'nfc_card_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'NFC karta ID raqami'}),
        }
        labels = {
            'first_name': 'Ismi',
            'last_name': 'Familiyasi',
            'middle_name': 'Otasining ismi',
            'phone': 'Telefon raqami',
            'birth_date': "Tug'ilgan sana",
            'branch': 'Filial',
            'avatar': 'Rasm',
            'nfc_card_id': 'NFC Karta ID (Turniket uchun)',
        }

    def save(self, commit=True, organization=None):
        user = super().save(commit=False)
        user.role = 'teacher'
        user.set_password(self.cleaned_data['password'])
        
        # Qo'shimcha ma'lumotlarni profile_data ga saqlash
        user.profile_data = {
            'passport_series': self.cleaned_data.get('passport_series', ''),
            'address': self.cleaned_data.get('address', ''),
        }
        
        if organization:
            user.organization = organization
            
        if commit:
            user.save()
        return user


# ============================================
# XODIM FORMASI (Staff) - ROL VA RUXSATLAR BILAN
# ============================================

# Mavjud bo'limlar va amallar
AVAILABLE_MODULES = [
    ('users', 'Foydalanuvchilar', 'ph-users'),
    ('education', 'Ta\'lim (Guruhlar, Kurslar)', 'ph-graduation-cap'),
    ('finance', 'Moliya (To\'lovlar, Xarajatlar)', 'ph-money'),
    ('crm', 'CRM (Lidlar, Voronka)', 'ph-funnel'),
    ('operations', 'Operatsiyalar (Darslar, Davomat)', 'ph-calendar'),
    ('reports', 'Hisobotlar', 'ph-chart-bar'),
    ('settings', 'Sozlamalar', 'ph-gear'),
]

AVAILABLE_ACTIONS = [
    ('view', 'Ko\'rish'),
    ('create', 'Yaratish'),
    ('edit', 'Tahrirlash'),
    ('delete', 'O\'chirish'),
]

# Xodim rollari
STAFF_ROLE_CHOICES = [
    ('admin', 'Administrator'),
    ('staff', 'Xodim'),
    ('owner', 'Direktor'),
]


class StaffForm(forms.ModelForm):
    """Xodim qo'shish formasi - rol va ruxsatlar bilan"""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '********'}),
        required=True, 
        label="Parol"
    )
    
    staff_role = forms.ChoiceField(
        choices=STAFF_ROLE_CHOICES,
        required=True,
        label="Lavozim",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    passport_series = forms.CharField(
        max_length=20, 
        required=False,
        label="Pasport seriyasi",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "AA1234567"})
    )
    
    address = forms.CharField(
        max_length=255, 
        required=False,
        label="Manzil",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "To'liq manzil"})
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'middle_name', 'phone', 
            'birth_date', 'branch', 'avatar', 'nfc_card_id'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ismi', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Familiyasi', 'required': True}),
            'middle_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Otasining ismi'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '998901234567', 'required': True}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'nfc_card_id': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'NFC karta ID raqami'}),
        }
        labels = {
            'first_name': 'Ismi',
            'last_name': 'Familiyasi',
            'middle_name': 'Otasining ismi',
            'phone': 'Telefon raqami',
            'birth_date': "Tug'ilgan sana",
            'branch': 'Filial',
            'avatar': 'Rasm',
            'nfc_card_id': 'NFC Karta ID',
        }

    def save(self, commit=True, organization=None, permissions=None):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('staff_role', 'staff')
        user.set_password(self.cleaned_data['password'])
        
        user.profile_data = {
            'passport_series': self.cleaned_data.get('passport_series', ''),
            'address': self.cleaned_data.get('address', ''),
        }
        
        # Ruxsatlarni saqlash
        if permissions:
            user.permissions = permissions

        if organization:
            user.organization = organization
            
        if commit:
            user.save()
        return user
