from flask_script import Shell
from flask_migrate import Manager, MigrateCommand
from services.config import db, migrate
from services.app import app
from services.resources import Calculation

manager = Manager(app)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    app.run(debug=True)
