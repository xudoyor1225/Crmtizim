"""
Finance moduli uchun signal'lar.
Transaction tasdiqlanganda balansni avtomatik yangilash.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from apps.finance.models import Transaction


@receiver(pre_save, sender=Transaction)
def prevent_edit_confirmed_transaction(sender, instance, **kwargs):
    """
    Tasdiqlangan tranzaksiyani o'zgartirishni oldini olish.
    Bu moliyaviy xatolarning oldini oladi.
    """
    if instance.pk:  # Mavjud obyekt (yangi emas)
        try:
            old_transaction = Transaction.objects.get(pk=instance.pk)

            # Agar status confirmed bo'lsa, muhim maydonlarni o'zgartirish mumkin emas
            if old_transaction.status == 'confirmed':
                critical_fields = ['amount', 'transaction_type', 'account', 'student', 'staff']

                for field in critical_fields:
                    old_value = getattr(old_transaction, field)
                    new_value = getattr(instance, field)

                    if old_value != new_value:
                        raise ValidationError(
                            f"Tasdiqlangan tranzaksiyaning '{field}' maydonini o'zgartirib bo'lmaydi! "
                            f"Agar xato bo'lsa, uni bekor qiling va yangisini yarating."
                        )
        except Transaction.DoesNotExist:
            pass  # Yangi obyekt


@receiver(post_save, sender=Transaction)
def update_balances_on_transaction(sender, instance, created, **kwargs):
    """
    Transaction tasdiqlanganda balanslarni avtomatik yangilash.

    Qoidalar:
    1. Faqat status='confirmed' bo'lganda balanslarga ta'sir qiladi
    2. O'quvchi to'lovi (income) -> student.balance OSHADI
    3. O'quvchi to'lovdan qaytarish (refund) -> student.balance KAMAYADI
    4. Xodim oyligi (salary) -> staff.balance (agar kerak bo'lsa)
    5. Kassa balance ham o'zgaradi
    """
    # Faqat tasdiqlangan tranzaksiyalar
    if instance.status != 'confirmed':
        return

    # Kassa balansini yangilash
    account = instance.account

    if instance.transaction_type == 'income':
        # Kirim - kassaga qo'shiladi
        account.balance += instance.amount

        # O'quvchi to'lovi bo'lsa, uning balansiga ham qo'shiladi
        if instance.student:
            instance.student.balance += instance.amount
            instance.student.save(update_fields=['balance'])

    elif instance.transaction_type == 'expense':
        # Chiqim - kassadan ayiriladi
        account.balance -= instance.amount

    elif instance.transaction_type == 'refund':
        # Pul qaytarish - kassadan chiqib ketadi
        account.balance -= instance.amount

        # O'quvchidan balans ayiriladi
        if instance.student:
            instance.student.balance -= instance.amount
            instance.student.save(update_fields=['balance'])

    elif instance.transaction_type == 'salary':
        # Xodim oyligi - kassadan chiqadi
        account.balance -= instance.amount

    elif instance.transaction_type == 'transfer':
        # O'tkazma logikasi (agar kerak bo'lsa)
        pass

    account.save(update_fields=['balance'])


@receiver(post_save, sender=Transaction)
def log_transaction_confirmation(sender, instance, created, **kwargs):
    """
    Transaction tasdiqlanishini audit log'ga yozish.
    """
    if not created and instance.status == 'confirmed':
        from apps.core.models import AuditLog

        AuditLog.log(
            user=instance.confirmed_by,
            action='UPDATE',
            model_name='Transaction',
            object_id=instance.id,
            object_repr=str(instance),
            changes={
                'status': 'confirmed',
                'amount': float(instance.amount),
                'type': instance.transaction_type
            }
        )
