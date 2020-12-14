# DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment beat
# set DJANGO_SETTINGS_MODULE=settings.local
# celery -A recruitment beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
