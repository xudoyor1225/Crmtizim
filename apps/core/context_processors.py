def tenant_context(request):
    """
    Barcha shablonlarga 'organization' o'zgaruvchisini qo'shadi.
    """
    return {
        'organization': request.organization
    }


def user_permissions_context(request):
    """
    Foydalanuvchi ruxsatlarini shablonlarga qo'shadi.
    """
    if not request.user.is_authenticated:
        return {
            'user_modules': [],
            'can_view': lambda m: False,
        }

    user = request.user

    # Super admin, owner, admin - hamma narsaga ruxsat
    if user.role in ['super_admin', 'owner', 'admin']:
        allowed_modules = ['dashboard', 'users', 'education', 'finance', 'crm', 'operations', 'reports', 'settings', 'automation']
        return {
            'user_modules': allowed_modules,
            'full_access': True,
        }

    # Boshqa rollar uchun permissions dan tekshirish
    allowed_modules = ['dashboard']  # Hammaga dashboard

    if user.permissions:
        for module, perms in user.permissions.items():
            if perms.get('view', False):
                allowed_modules.append(module)

    return {
        'user_modules': allowed_modules,
        'full_access': False,
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
