from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
import telebot
import os

@shared_task
def backup_and_report():
    # 1. Baza nusxasini olish
    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M')
    backup_file = f"backup_{timestamp}.json"

    with open(backup_file, 'w', encoding='utf-8') as f:
        call_command('dumpdata', exclude=['contenttypes', 'auth.permission'], stdout=f)

    # 2. Telegramga yuborish
    if settings.TELEGRAM_BOT_TOKEN:
        try:
            bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
            # Super Admin ID sini settingsdan olish kerak yoki statik yozish kerak
            # Hozircha logga yozamiz
            print(f"Backup tayyor: {backup_file}")

            # Agar Admin ID bo'lsa:
            # bot.send_document(ADMIN_ID, open(backup_file, 'rb'), caption=f"📅 Kunlik Backup: {timestamp}")

        except Exception as e:
            print(f"Telegram error: {e}")

    # 3. Faylni o'chirish (joyni tejash)
    # os.remove(backup_file) 
    return "Backup sent!"
