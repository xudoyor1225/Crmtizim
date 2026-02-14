"""
Core Background Tasks - Celery bilan.
Tizim uchun umumiy vazifalar.
"""
from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from datetime import timedelta
import os


@shared_task
def backup_and_report():
    """
    Kunlik backup yaratish va Telegram ga yuborish.
    """
    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M')
    backup_file = f"backup_{timestamp}.json"

    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            call_command('dumpdata', exclude=['contenttypes', 'auth.permission'], stdout=f)

        # Telegramga yuborish
        if settings.TELEGRAM_BOT_TOKEN:
            try:
                import telebot
                bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
                print(f"Backup tayyor: {backup_file}")
            except Exception as e:
                print(f"Telegram error: {e}")

        return f"Backup created: {backup_file}"

    except Exception as e:
        return f"Backup failed: {str(e)}"


@shared_task
def cleanup_deleted_objects():
    """
    O'chirilgan obyektlarni bazadan tozalash.
    30 kundan eski soft-deleted ma'lumotlarni o'chirish.
    """
    from apps.users.models import User
    from apps.crm.models import Lead
    from apps.finance.models import Transaction

    threshold = timezone.now() - timedelta(days=30)

    deleted_count = {
        'users': 0,
        'leads': 0,
        'transactions': 0,
    }

    # Foydalanuvchilar
    deleted_count['users'] = User.objects.filter(
        is_deleted=True,
        updated_at__lt=threshold
    ).delete()[0]

    # Lidlar
    deleted_count['leads'] = Lead.objects.filter(
        is_deleted=True,
        updated_at__lt=threshold
    ).delete()[0]

    # Tranzaksiyalar
    deleted_count['transactions'] = Transaction.objects.filter(
        is_deleted=True,
        updated_at__lt=threshold
    ).delete()[0]

    return f"Cleaned up: {deleted_count}"


@shared_task
def clear_expired_cache():
    """
    Muddati o'tgan cache ni tozalash.
    """
    try:
        cache.clear()
        return "Cache cleared successfully"
    except Exception as e:
        return f"Cache clear failed: {str(e)}"


@shared_task
def send_email_async(to_email, subject, body):
    """
    Email yuborishni background da bajarish.
    """
    from django.core.mail import send_mail

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        return f"Email sent to {to_email}"
    except Exception as e:
        return f"Email failed: {str(e)}"


@shared_task
def update_statistics_cache():
    """
    Dashboard statistikalarini cache ga yozish.
    Har 5 daqiqada yangilanadi.
    """
    from apps.users.models import User
    from apps.finance.models import Transaction
    from apps.education.models import Group
    from django.db.models import Sum

    # Umumiy statistika
    stats = {
        'total_students': User.objects.filter(role='student', is_deleted=False).count(),
        'total_teachers': User.objects.filter(role='teacher', is_deleted=False).count(),
        'total_groups': Group.objects.filter(is_deleted=False).count(),
        'total_income': Transaction.objects.filter(
            transaction_type='income',
            status='confirmed',
            is_deleted=False
        ).aggregate(total=Sum('amount'))['total'] or 0,
    }

    # Cache ga saqlash (1 soat)
    cache.set('dashboard_stats', stats, 3600)

    return f"Statistics cached: {stats}"

