import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# Настройка периодических задач
app.conf.beat_schedule = {
    'send-habit-notifications': {
        'task': 'habits.tasks.send_notifications',
        'schedule': crontab(minute='*'),  # Выполнять каждую минуту
    },
}
