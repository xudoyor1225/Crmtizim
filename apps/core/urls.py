from django.urls import path
from apps.core.history_views import history_list, history_detail
from apps.core.settings_views import settings_index

app_name = 'core'

urlpatterns = [
    path('history/', history_list, name='history_list'),
    path('history/<int:log_id>/', history_detail, name='history_detail'),
    path('settings/', settings_index, name='settings'),
]
