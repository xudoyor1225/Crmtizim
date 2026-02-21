from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.finance.models import Transaction, CashSubmission

@transaction.atomic
def confirm_transaction(transaction_id, user):
    """
    Tranzaksiyani xavfsiz tasdiqlash.
    Bazaviy qoidalar:
    1. Tranzaksiya qulflanadi (select_for_update) - bir vaqtda ikki marta bosilmasligi uchun.
    2. Status 'pending' bo'lsagina ishlaydi.
    3. Balanslar signal orqali atomik tarzda yangilanadi (signals.py).
    """
    try:
        # DB ni qulflaymiz
        tx = Transaction.objects.select_for_update().get(id=transaction_id)
    except Transaction.DoesNotExist:
        raise ValidationError("Tranzaksiya topilmadi.")

    if tx.status == 'confirmed':
        return tx

    # Chiqim uchun yetarli mablag' tekshirish
    if tx.transaction_type in ['expense', 'salary', 'refund']:
        tx.account.refresh_from_db()
        if tx.account.balance < tx.amount:
            raise ValidationError(f"Kassada mablag' yetarli emas! Mavjud: {tx.account.balance}")

    # Status o'zgartirish - balanslar signal orqali yangilanadi
    tx.status = 'confirmed'
    tx.confirmed_by = user
    tx.confirmed_at = timezone.now()
    tx.receipt_verified = True
    tx.receipt_verified_by = user
    tx.receipt_verified_at = timezone.now()

    tx.save()

    return tx


@transaction.atomic
def approve_cash_submission(submission_id, user):
    """
    Kassa topshirishni tasdiqlash.
    Admin kassasidan asosiy kassaga pul o'tkazish.

    Qoidalar:
    1. Submission qulflanadi (select_for_update).
    2. Status 'pending' bo'lsagina ishlaydi.
    3. Admin kassasidan pul ayiriladi, asosiy kassaga qo'shiladi.
    4. Transfer tranzaksiya yaratiladi.
    """
    try:
        submission = CashSubmission.objects.select_for_update().get(id=submission_id)
    except CashSubmission.DoesNotExist:
        raise ValidationError("Topshirish topilmadi.")

    if submission.status != 'pending':
        raise ValidationError("Bu topshirish allaqachon ko'rib chiqilgan.")

    net_amount = submission.net_amount

    # Admin kassasidan pul ayirish
    admin_account = submission.admin_account
    if net_amount > 0 and admin_account.balance < net_amount:
        raise ValidationError(
            f"Admin kassasida mablag' yetarli emas! Mavjud: {admin_account.balance}, Kerak: {net_amount}"
        )

    if net_amount > 0:
        admin_account.balance -= net_amount
        admin_account.save()

        # Asosiy kassaga transfer tranzaksiya yaratish (signal orqali balans yangilanadi)
        Transaction.objects.create(
            organization=submission.organization,
            account=submission.main_account,
            amount=net_amount,
            transaction_type='income',
            description=f"Kassa topshirish: {submission.admin_user.get_full_name()} "
                        f"({submission.get_period_type_display()}: {submission.period_start} - {submission.period_end})",
            status='confirmed',
            created_by=submission.admin_user,
            confirmed_by=user,
            confirmed_at=timezone.now(),
            payment_method='transfer',
        )

    # Submission statusini yangilash
    submission.status = 'approved'
    submission.approved_by = user
    submission.approved_at = timezone.now()
    submission.save()

    # Admin ga bildirishnoma yuborish
    try:
        from apps.automation.services import create_system_notification
        create_system_notification(
            recipient=submission.admin_user,
            title="Kassa topshirish tasdiqlandi ✅",
            message=(
                f"Sizning {submission.period_start.strftime('%d.%m.%Y')} - "
                f"{submission.period_end.strftime('%d.%m.%Y')} oralig'idagi "
                f"kassa topshirishingiz tasdiqlandi. "
                f"Sof summa: {net_amount:,.0f} so'm. "
                f"Tasdiqlagan: {user.get_full_name()}"
            ),
            notification_type='system'
        )
    except Exception:
        pass  # Bildirishnoma xatosi asosiy jarayonni to'xtatmasligi kerak

    return submission
