def tenant_context(request):
    """
    Barcha shablonlarga 'organization' o'zgaruvchisini qo'shadi.
    """
    return {
        'organization': request.organization
    }


def notifications_context(request):
    """
    Barcha shablonlarga bildirishnomalarni qo'shadi.
    """
    if not request.user.is_authenticated:
        return {
            'notifications': [],
            'unread_notifications_count': 0
        }

    try:
        from apps.automation.models import NotificationLog

        # Foydalanuvchining oxirgi 10 ta bildirishnomasini olish
        notifications = NotificationLog.objects.filter(
            recipient=request.user,
            is_deleted=False
        ).select_related('template').order_by('-created_at')[:10]

        # O'qilmagan bildirishnomalar soni
        unread_count = NotificationLog.objects.filter(
            recipient=request.user,
            is_deleted=False,
            status='sent'
        ).count()

        return {
            'notifications': notifications,
            'unread_notifications_count': unread_count
        }
    except Exception:
        return {
            'notifications': [],
            'unread_notifications_count': 0
        }
