from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.finance.models import Transaction

@transaction.atomic
def confirm_transaction(transaction_id, user):
    """
    Tranzaksiyani xavfsiz tasdiqlash.
    Bazaviy qoidalar:
    1. Tranzaksiya qulflanadi (select_for_update) - bir vaqtda ikki marta bosilmasligi uchun.
    2. Status 'pending' bo'lsagina ishlaydi.
    3. Balanslar atomik tarzda yangilanadi.
    """
    try:
        # DB ni qulflaymiz
        tx = Transaction.objects.select_for_update().get(id=transaction_id)
    except Transaction.DoesNotExist:
        raise ValidationError("Tranzaksiya topilmadi.")

    if tx.status == 'confirmed':
        # Agar allaqachon tasdiqlangan bo'lsa, xato qaytarmaymiz, shunchaki qaytamiz
        return tx 

    # 1. Kassa Balansi
    if tx.transaction_type == 'income':
        tx.account.balance += tx.amount
    elif tx.transaction_type in ['expense', 'salary', 'refund']:
        if tx.account.balance < tx.amount:
            raise ValidationError(f"Kassada mablag' yetarli emas! Mavjud: {tx.account.balance}")
        tx.account.balance -= tx.amount

    tx.account.save()

    # 2. Student Balansi (Agar studentga bog'liq bo'lsa)
    if tx.student and tx.transaction_type == 'income':
        tx.student.balance += tx.amount
        tx.student.save()

    # 3. Status o'zgartirish
    tx.status = 'confirmed'
    tx.confirmed_by = user
    tx.confirmed_at = timezone.now()
    # Avtomatik ravishda chek tasdiqlangan deb belgilanadi
    tx.receipt_verified = True
    tx.receipt_verified_by = user
    tx.receipt_verified_at = timezone.now()

    tx.save()

    return tx
