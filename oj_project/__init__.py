from __future__ import absolute_import, unicode_literals

# This imports the Celery app when Django starts
from .celery import app as celery_app

__all__ = ('celery_app',)

#Meaning: “Hey Django, when you start, also start Celery!”