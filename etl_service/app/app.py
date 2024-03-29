from flask import Flask, jsonify
from flask_uploads import configure_uploads

from .services import services_senders as s
from .api import api_1_0_blueprint
from .config import FlaskConfig
from .resources import csv_uploader


def custom_exception(error):
    response = jsonify({'message': error.description})
    response.status_code = 400
    return response


def register_errors(app_, errors_codes):
    for errors_code in errors_codes:
        app_.error_handler_spec[errors_code] = custom_exception
    return app_


def create_app():
    app_init = Flask(__name__)
    app_init.config.from_object(FlaskConfig)
    app_init.register_blueprint(api_1_0_blueprint, url_prefix='/api')
    configure_uploads(app_init, (csv_uploader,))
    register_errors(app_init, (300, 400))
    app_init.projects = s.ProjectService()
    app_init.session_handler = s.SessionService()
    return app_init


app = create_app()
