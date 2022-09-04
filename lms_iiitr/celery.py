from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
   # setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_iiitr.settings')
app = Celery('lms_iiitr')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

#Celery Beat settings
app.conf.beat_schedule = {
    # Executes everyday a 12 a.m.
    'update-every-day': {
        'task': 'oauth_app.tasks.test_func',
        'schedule':crontab(), #crontab(minute=0, hour=0),

        # 'args': (16, 16),
    }
}

    # Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()

@app.task(bind = True)
def debug_task(self):
    print(f'Request: {self.request!r}')
