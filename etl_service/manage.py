from flask_script import Manager

from app.app import app

manager = Manager(app)


@manager.option('-p', '--port', dest='port', default=5000)
@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-d', '--debug', dest='debug', default=False)
def runserver(host, port, debug):
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    manager.run()
