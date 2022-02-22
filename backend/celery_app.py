from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery()

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send_notifications': {
        'task': 'notifications.tasks.send_notifications',
        'schedule': 2.0,
    },
}
app.conf.timezone = 'UTC'