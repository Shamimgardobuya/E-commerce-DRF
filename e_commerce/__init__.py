from .celery import app as celery_app

__all__  = ("celery_app",) #ensures that the shared task decorator will use it correctly