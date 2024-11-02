import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','restful_ecom.settings')

celery = Celery('restful_ecom')
celery.config_from_object('django.conf:settings',namespace='CELERY')
celery.autodiscover_tasks()