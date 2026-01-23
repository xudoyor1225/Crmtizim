import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Har kuni soat 23:59 da ishlaydigan vazifa
app.conf.beat_schedule = {
    'daily-database-backup': {
        'task': 'apps.core.tasks.backup_and_report',
        'schedule': crontab(hour=23, minute=59),
    },
}
