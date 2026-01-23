from django.conf import settings
from .models import NotificationTemplate, NotificationLog
from apps.users.models import User
import logging

logger = logging.getLogger(__name__)

def send_notification(user: User, template_code: str, context: dict = None):
    """
    Foydalanuvchiga xabar yuborish.
    
    Args:
        user: Qabul qiluvchi user
        template_code: Shablon kodi (masalan: 'payment_received')
        context: Xabar ichidagi o'zgaruvchilar (masalan: {'amount': 1000})
    """
    if context is None:
        context = {}
        
    # User haqida ma'lumotlarni contextga qo'shamiz
    context.update({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
    })

    try:
        # Shablonni topish
        template = NotificationTemplate.objects.filter(code=template_code, is_deleted=False).first()
        
        if not template:
            logger.warning(f"Notification template not found: {template_code}")
            return False

        # Xabarni shakllantirish
        try:
            message_body = template.body.format(**context)
        except KeyError as e:
            logger.error(f"Missing context key for template {template_code}: {e}")
            message_body = template.body # Formatlashsiz qaytaramiz

        # Telegram yuborish
        if template.message_type == 'telegram' and settings.TELEGRAM_BOT_TOKEN:
            try:
                import telebot
                bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
                
                if user.telegram_id:
                    bot.send_message(user.telegram_id, message_body, parse_mode='HTML')
                    status = 'sent'
                else:
                    logger.warning(f"User {user} has no telegram_id")
                    status = 'failed'
            except Exception as e:
                logger.error(f"Telegram error: {e}")
                status = 'failed'
        else:
             # SMS (Mock) yoki System
             status = 'sent'

        # Log yozish
        NotificationLog.objects.create(
            organization=user.organization,
            recipient=user,
            template=template,
            message=message_body,
            message_type=template.message_type,
            status=status
        )
        
        print(f"NOTIFICATION SENT [{template.message_type}] to {user.phone}: {message_body}")
        return True

    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return False
