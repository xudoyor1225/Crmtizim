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
            'full_access': False,
        }

    user = request.user

    # Super admin va owner - hamma narsaga ruxsat
    if user.role in ['super_admin', 'owner']:
        allowed_modules = ['dashboard', 'users', 'education', 'finance', 'crm', 'operations', 'reports', 'settings', 'automation']
        return {
            'user_modules': allowed_modules,
            'full_access': True,
        }

    # Admin, staff va boshqa rollar uchun permissions dan tekshirish
    allowed_modules = ['dashboard']  # Hammaga dashboard

    # Agar permissions bo'sh bo'lsa va admin bo'lsa - hamma narsaga ruxsat
    if user.role == 'admin' and not user.permissions:
        allowed_modules = ['dashboard', 'users', 'education', 'finance', 'crm', 'operations', 'reports', 'settings', 'automation', 'admin_finance']
        return {
            'user_modules': allowed_modules,
            'full_access': True,
        }

    # O'qituvchi - default modullar
    if user.role == 'teacher' and not user.permissions:
        allowed_modules = ['dashboard', 'operations', 'education']
        return {
            'user_modules': allowed_modules,
            'full_access': False,
        }

    # Permissions dan tekshirish
    if user.permissions:
        for module, perms in user.permissions.items():
            if isinstance(perms, dict) and perms.get('view', False):
                allowed_modules.append(module)

    # Admin uchun admin_finance har doim qo'shiladi
    if user.role == 'admin' and 'admin_finance' not in allowed_modules:
        allowed_modules.append('admin_finance')

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
