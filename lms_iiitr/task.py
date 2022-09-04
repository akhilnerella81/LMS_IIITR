from celery import Celery
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-day': {
        'task': 'tasks.add',
        'schedule': crontab(minute=0, hour=0),
        'args': (16, 16),
    },
}

#app.conf.timezone = 'UTC'
