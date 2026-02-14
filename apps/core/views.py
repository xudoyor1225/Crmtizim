"""
Core Views - Async bilan optimizatsiya qilingan.
Django 4.1+ async view'larni qo'llab-quvvatlaydi.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from asgiref.sync import sync_to_async
from .dashboards import role_based_dashboard


# Async helper functions
@sync_to_async
def get_notifications_page(user, page_num):
    from apps.automation.models import NotificationLog

    notifications = NotificationLog.objects.filter(
        recipient=user,
        is_deleted=False
    ).select_related('template').order_by('-created_at')

    paginator = Paginator(notifications, 20)
    return paginator.get_page(page_num)


@sync_to_async
def get_notification_by_pk(pk, user):
    from apps.automation.models import NotificationLog
    return NotificationLog.objects.get(pk=pk, recipient=user)


@sync_to_async
def mark_notification_read(notification):
    if notification.status == 'sent':
        notification.status = 'read'
        notification.save(update_fields=['status'])


@sync_to_async
def mark_all_notifications_read(user):
    from apps.automation.models import NotificationLog
    return NotificationLog.objects.filter(
        recipient=user,
        status='sent'
    ).update(status='read')


@login_required
def dashboard_view(request):
    """
    Bosh sahifa - roliga qarab dashboard ko'rsatadi.
    """
    return role_based_dashboard(request)


def logout_view(request):
    """Custom logout view - chiroyli sahifa ko'rsatadi"""
    logout(request)
    return render(request, 'registration/logged_out.html')


@login_required
async def notifications_list(request):
    """
    Barcha bildirishnomalar ro'yxati (ASYNC)
    """
    page = request.GET.get('page', 1)
    notifications = await get_notifications_page(request.user, page)

    return render(request, 'core/notifications.html', {
        'notifications': notifications,
    })


@login_required
@require_http_methods(["GET", "POST"])
async def notification_read(request, pk):
    """
    Bildirishnomani o'qildi deb belgilash (ASYNC)
    """
    try:
        notification = await get_notification_by_pk(pk, request.user)
        await mark_notification_read(notification)
    except Exception:
        pass

    # Agar redirect URL berilgan bo'lsa
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)

    return redirect('core:notifications')


@login_required
@require_http_methods(["POST"])
async def notifications_mark_all_read(request):
    """
    Barcha bildirishnomalarni o'qildi deb belgilash (ASYNC)
    """
    await mark_all_notifications_read(request.user)

    messages.success(request, "Barcha bildirishnomalar o'qildi deb belgilandi")
    return redirect('core:notifications')

