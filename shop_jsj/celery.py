import os

from celery import Celery

# Настройки Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_jsj.settings")
app = Celery("shop_jsj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
