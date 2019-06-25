from flask import Flask
from api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api import models

from api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run()
