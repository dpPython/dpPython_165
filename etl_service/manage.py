import sys
import os
import coverage

from app.app import app

from flask_script import Manager

manager = Manager(app)


if os.environ.get('FLASK_COVERAGE'):
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@manager.option('-p', '--port', dest='port', default=5000)
@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-d', '--debug', dest='debug', default=False)
def runserver(host, port, debug):
    app.run(host=host, port=port, debug=debug)


@manager.command
def test(coverage_=False):
    if coverage_ and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()
