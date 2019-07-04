from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .api import usr_api

db = SQLAlchemy()
migrate = Migrate()


def psgres_url():
    return 'postgresql://postgres:11111111@localhost:5432/users'

def create_app():
    app = Flask(__name__)
    usr_api.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = psgres_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
    return app

bcrypt = Bcrypt(create_app())
