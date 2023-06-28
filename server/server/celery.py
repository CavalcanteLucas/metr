import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server', include=['measurements.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
