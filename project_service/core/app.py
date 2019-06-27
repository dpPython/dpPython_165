from .config import create_app
from .api import api_blueprint, api
from .controller import DataHandler, ProjectsInitializer, ProjectsResources, StatusUpdater

app = create_app()
app.register_blueprint(api_blueprint)

api.add_resource(ProjectsInitializer, '/projects')
api.add_resource(ProjectsResources, '/projects/<id>')

api.add_resource(DataHandler, '/projects/data/<id>')
api.add_resource(StatusUpdater, '/projects/status/<id>')
