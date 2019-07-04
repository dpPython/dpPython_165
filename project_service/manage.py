from flask_script import Manager, Server
from flask_migrate import MigrateCommand

from core.app import app

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host='0.0.0.0', port=5000))

if __name__ == '__main__':
    manager.run()
