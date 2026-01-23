import uuid
from django.db import models
from django.utils import timezone
from apps.core.middleware import get_current_organization

class BaseModel(models.Model):
    """
    Barcha modellar uchun umumiy maydonlar:
    - ID o'rniga UUID (Xavfsizlik uchun)
    - Yaratilgan vaqt
    - O'zgarish vaqti
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")

    class Meta:
        abstract = True


class SoftDeleteModel(BaseModel):
    """
    Ma'lumotni o'chirmasdan 'yashirish' (Trash can) funksiyasi.
    ERP tizimda hech narsa butunlay o'chmasligi kerak.
    """
    is_deleted = models.BooleanField(default=False, verbose_name="O'chirilganmi?")
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        # Haqiqiy o'chirish o'rniga, bayroqchani ko'tarib qo'yamiz
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        # Qayta tiklash
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class TenantAwareModel(SoftDeleteModel):
    """
    SaaS arxitekturasining yuragi.
    Ma'lumotni avtomatik ravishda tegishli O'quv Markazga bog'laydi.
    """
    # String reference ishlatamiz ('apps.organizations.Organization'),
    # chunki Organization hali yuklanmagan bo'lishi mumkin.
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name="%(class)s_related",
        verbose_name="Tashkilot",
        null=True, blank=True # SuperAdmin ma'lumotlari uchun bo'sh qolishi mumkin
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Agar tashkilot biriktirilmagan bo'lsa, uni avtomatik topamiz
        if not self.organization_id:
            org = get_current_organization()
            if org:
                self.organization = org
        super().save(*args, **kwargs)


class AuditLog(models.Model):
    """
    Barcha o'zgarishlarni kuzatish uchun log.
    Kim, qachon, nimani o'zgartirdi - hammasini saqlaymiz.
    """
    ACTION_CHOICES = (
        ('CREATE', 'Yaratildi'),
        ('UPDATE', 'O\'zgartirildi'),
        ('DELETE', 'O\'chirildi'),
        ('LOGIN', 'Tizimga kirdi'),
        ('LOGOUT', 'Tizimdan chiqdi'),
    )

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='audit_logs'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name="Kim bajardi"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Amal")
    model_name = models.CharField(max_length=100, verbose_name="Model nomi")
    object_id = models.IntegerField(null=True, blank=True, verbose_name="Obyekt ID")
    object_repr = models.CharField(max_length=255, blank=True, verbose_name="Obyekt nomi")
    changes = models.JSONField(default=dict, blank=True, verbose_name="O'zgarishlar")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Manzil")
    user_agent = models.CharField(max_length=500, blank=True, verbose_name="Brauzer")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqt")

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Loglar"

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"

    @classmethod
    def log(cls, user, action, model_name, object_id=None, object_repr='', changes=None, request=None):
        """
        Log yozish uchun helper method.
        """
        log_entry = cls(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            object_repr=object_repr[:255] if object_repr else '',
            changes=changes or {},
        )
        
        if user and hasattr(user, 'organization'):
            log_entry.organization = user.organization
            
        if request and hasattr(request, 'organization') and request.organization:
            log_entry.organization = request.organization
            
        if request:
            log_entry.ip_address = cls.get_client_ip(request)
            log_entry.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        log_entry.save()
        return log_entry

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip