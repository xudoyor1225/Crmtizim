"""
Custom template tags for role checking.
"""
from django import template

register = template.Library()


@register.filter(name='has_role')
def has_role(user, roles):
    """
    Foydalanuvchining roli berilgan rollar ichida borligini tekshirish.

    Foydalanish:
        {% if request.user|has_role:"admin,owner,teacher" %}
            ...
        {% endif %}
    """
    if not user or not user.is_authenticated:
        return False

    role_list = [r.strip() for r in roles.split(',')]
    return user.role in role_list


@register.simple_tag(takes_context=True)
def user_can(context, *roles):
    """
    Foydalanuvchining roli berilgan rollardan biriga mos kelishini tekshirish.

    Foydalanish:
        {% user_can 'admin' 'owner' as can_manage %}
        {% if can_manage %}
            ...
        {% endif %}
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False

    return request.user.role in roles


@register.filter(name='is_admin')
def is_admin(user):
    """Admin yoki yuqori rolni tekshirish"""
    return user.is_authenticated and user.role in ['super_admin', 'owner', 'admin']


@register.filter(name='is_teacher_or_admin')
def is_teacher_or_admin(user):
    """O'qituvchi yoki admin rolni tekshirish"""
    return user.is_authenticated and user.role in ['super_admin', 'owner', 'admin', 'teacher']


@register.filter(name='is_staff_member')
def is_staff_member(user):
    """Xodim rolini tekshirish"""
    return user.is_authenticated and user.role in ['super_admin', 'owner', 'admin', 'teacher', 'staff']


# ============================================
# MODUL ASOSIDAGI RUXSATLAR (Yangi)
# ============================================

@register.simple_tag(takes_context=True)
def has_permission(context, module, action='view'):
    """
    Foydalanuvchining modul va amal bo'yicha ruxsatini tekshirish.

    Foydalanish:
        {% has_permission 'finance' 'create' as can_create %}
        {% if can_create %}
            <a href="...">Yaratish</a>
        {% endif %}

        yoki:
        {% has_permission 'users' 'delete' as can_delete %}
        {% if not can_delete %}
            <span class="text-red-500">Ruxsat yo'q</span>
        {% endif %}
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return False

    user = request.user

    # Super admin va owner - hamma narsaga ruxsat
    if user.role in ['super_admin', 'owner']:
        return True

    # Admin - agar permissions bo'sh bo'lsa, ruxsat bor
    if user.role == 'admin' and not user.permissions:
        return True

    # Permissions tekshirish
    if user.permissions:
        module_perms = user.permissions.get(module, {})
        if isinstance(module_perms, dict):
            return module_perms.get(action, False)

    return False


@register.inclusion_tag('components/permission_button.html', takes_context=True)
def permission_button(context, module, action, url, text, icon='', css_class=''):
    """
    Ruxsatga qarab tugma ko'rsatish yoki "Ruxsat yo'q" chiqarish.

    Foydalanish:
        {% permission_button 'finance' 'create' url text='Yaratish' icon='ph-plus' %}
    """
    request = context.get('request')
    has_perm = False

    if request and request.user.is_authenticated:
        user = request.user
        if user.role in ['super_admin', 'owner']:
            has_perm = True
        elif user.role == 'admin' and not user.permissions:
            has_perm = True
        elif user.permissions:
            module_perms = user.permissions.get(module, {})
            if isinstance(module_perms, dict):
                has_perm = module_perms.get(action, False)

    return {
        'has_permission': has_perm,
        'url': url,
        'text': text,
        'icon': icon,
        'css_class': css_class,
        'module': module,
        'action': action,
    }


