from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from .api import api_blueprint, api


DBUSER = 'postgres'
DBPASS = ''
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'postgres'

db = SQLAlchemy()
migrate = Migrate()


def postgres_uri():
    # if os.getenv("DOCKER"):
        # return 'postgresql://postgres@db_projects_service:5432/postgres'
    return 'postgresql://eugene:1401@localhost/projects'
    # return 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
    #         user=DBUSER,
    #         passwd=DBPASS,
    #         host=DBHOST,
    #         port=DBPORT,
    #         db=DBNAME)


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'
    SQLALCHEMY_DATABASE_URI = 'postgresql://eugene:1401@localhost/projects'


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://eugene:1401@localhost/projects'


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    return app
