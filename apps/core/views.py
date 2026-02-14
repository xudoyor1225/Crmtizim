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
def notifications_list(request):
    """
    Barcha bildirishnomalar ro'yxati
    """
    from apps.automation.models import NotificationLog

    notifications = NotificationLog.objects.filter(
        recipient=request.user,
        is_deleted=False
    ).select_related('template').order_by('-created_at')

    # Pagination
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page', 1)
    notifications = paginator.get_page(page)

    return render(request, 'core/notifications.html', {
        'notifications': notifications,
    })


@login_required
@require_http_methods(["GET", "POST"])
def notification_read(request, pk):
    """
    Bildirishnomani o'qildi deb belgilash
    """
    from apps.automation.models import NotificationLog

    notification = get_object_or_404(NotificationLog, pk=pk, recipient=request.user)

    # O'qildi deb belgilash
    if notification.status == 'sent':
        notification.status = 'read'
        notification.save(update_fields=['status'])  # Optimizatsiya

    # Agar redirect URL berilgan bo'lsa
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)

    return redirect('core:notifications')


@login_required
@require_http_methods(["POST"])
def notifications_mark_all_read(request):
    """
    Barcha bildirishnomalarni o'qildi deb belgilash
    """
    from apps.automation.models import NotificationLog

    NotificationLog.objects.filter(
        recipient=request.user,
        status='sent'
    ).update(status='read')

    messages.success(request, "Barcha bildirishnomalar o'qildi deb belgilandi")
    return redirect('core:notifications')

