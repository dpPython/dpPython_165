from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from .api import api

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    api.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://calc_manager:1234@localhost/calculation'
    # app.register_blueprint(api_blueprint,  url_prefix='/calculate')
    with app.app_context():
        db.init_app(app)
    migrate.init_app(app=app, db=db)
    return app