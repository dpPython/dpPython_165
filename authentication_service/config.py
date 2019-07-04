import os
from flask import Flask
from flask_redis import FlaskRedis
from mockredis import MockRedis
from services.api_1_0 import api_auth_blueprint


class FlaskConfig:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'uploads')
    REDIS_URL = "redis://:redis@localhost:6379/0"


def create_app():
    app = Flask(__name__)
    if app.testing:
        redis_client = FlaskRedis.from_custom_provider(MockRedis)
    else:
        redis_client = FlaskRedis()
    app.config.from_object(FlaskConfig)
    app.register_blueprint(api_auth_blueprint,  url_prefix='/auth')
    redis_client.init_app(app)
    return app
