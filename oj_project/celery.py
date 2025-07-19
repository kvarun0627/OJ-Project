from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# This tells Django to use settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oj_project.settings')

# Create the Celery app and call it 'oj_project'
app = Celery('oj_project')

# Load config from Django settings, prefixed with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks.py in all apps
app.autodiscover_tasks()

#Think of this like “Celery’s brain” — it knows what tasks to run