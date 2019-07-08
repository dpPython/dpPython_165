from flask import Flask


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from core.models import db
    db.init_app(app)

    from core.views import api_bp
    app.register_blueprint(api_bp, url_prefix='/contracts')

    return app
