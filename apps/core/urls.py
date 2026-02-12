from django.urls import path
from apps.core.history_views import history_list, history_detail
from apps.core.settings_views import settings_index
from apps.core.views import notifications_list, notification_read, notifications_mark_all_read

app_name = 'core'

urlpatterns = [
    path('history/', history_list, name='history_list'),
    path('history/<int:log_id>/', history_detail, name='history_detail'),
    path('settings/', settings_index, name='settings'),

    # Bildirishnomalar
    path('notifications/', notifications_list, name='notifications'),
    path('notifications/<int:pk>/read/', notification_read, name='notification_read'),
    path('notifications/mark-all-read/', notifications_mark_all_read, name='notifications_mark_all_read'),
]
