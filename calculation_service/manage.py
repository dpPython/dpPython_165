from flask_script import Shell, Server
from flask_migrate import Manager, MigrateCommand
from services.config import db, migrate
from services.app import app
from services.resources import Calculation

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)
