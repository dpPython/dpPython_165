from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .api import api

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    ma = Marshmallow(app)
    api.init_app(app)
    app.config['CELERY_BROKER_URL'] = 'amqp://calc_manager:1234@localhost:port//vhost'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://calc_manager:1234@localhost/calculation'
    with app.app_context():
        db.init_app(app)
    migrate.init_app(app=app, db=db)
    return app
