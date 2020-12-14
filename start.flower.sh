
# set DJANGO_SETTINGS_MODULE=settings.local
# celery -A recruitment flower --broker=redis://localhost:6379/0
DJANGO_SETTINGS_MODULE=settings.production celery -A recruitment flower
