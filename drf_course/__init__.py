from .celery import app as celery_app

__all__ = ('celery_app',)
# This will ensure that the Celery app is always imported when
# Django starts so that shared_task will use this app.