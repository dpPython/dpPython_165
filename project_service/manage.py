from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from core.app import app
from core.config import db

from core.models import Projects, Data

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, Projects=Projects, RoomsData=Data)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
