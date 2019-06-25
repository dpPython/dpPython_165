from flask_script import Shell
from flask_migrate import MigrateCommand, Manager
from celery import Celery
from services.config import db, migrate
from services.app import app
from services.resources import Calculation

manager = Manager(app)
# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery






def make_shell_context():
    return dict(app=app, db=db, Calculations=Calculation)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)