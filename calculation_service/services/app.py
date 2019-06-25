from .config import create_app
from .api import api_blueprint, api
from .resources import Calculate

app = create_app()

api.add_resource(Calculate, '/')
app.register_blueprint(api_blueprint, url_prefix="/api")

