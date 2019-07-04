from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from .api import api


DBUSER = 'postgres'
DBPASS = ''
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'postgres'

db = SQLAlchemy()
migrate = Migrate()


def postgres_uri():
    # if os.getenv("DOCKER"):
    #     return 'postgresql://postgres@db_projects_service:5432/postgres'
    # return 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
    #         user=DBUSER,
    #         passwd=DBPASS,
    #         host=DBHOST,
    #         port=DBPORT,
    #         db=DBNAME)
    return 'postgresql://arthur:arthur234@localhost/projects'


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    return app
