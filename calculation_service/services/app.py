from .config import create_app
from .api import api_blueprint, api
from .resources import Calculate, Results

app = create_app()

api.add_resource(Calculate, '/process')
api.add_resource(Results, '/results')
app.register_blueprint(api_blueprint, url_prefix="/calculation")

