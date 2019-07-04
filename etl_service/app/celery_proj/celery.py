from celery import Celery, Task

celery = Celery('app.celery_proj.celery',broker='pyamqp://guest:guest@192.168.99.102:32793', backend='amqp://guest:guest@192.168.99.102:32793')
	
#celery.config_from_object('app.celery_proj.celeryconfig')
celery.autodiscover_tasks(['app.celery_proj.tasks'])
