'''
import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # url = 'postgresql://{}:{}@{}:{}/{}'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:11111111@localhost:5432/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from core.api import usr_api, bp

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    usr_api.init_app(app)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:11111111@localhost:5432/users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(bp, url_prefix='/users')
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
    return app
