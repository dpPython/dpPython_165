from celery import Celery

celery = Celery('app.celery_proj',
                broker='pyamqp://guest@192.168.99.102:32769')

celery.config_from_object('app.celery_proj.celeryconfig')
celery.autodiscover_tasks(['app.celery_proj.tasks'])

