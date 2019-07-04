from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

from core.app import app
from core.config import db
from core.models import Users

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, Users=Users)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
