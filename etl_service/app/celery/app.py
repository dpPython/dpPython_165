from celery import Celery
import app.celery.celeryconfig as cf

celery_app = Celery('tasks', broker='pyamqp://guest@192.168.99.101:32769/')

celery_app.config_from_object(cf)
