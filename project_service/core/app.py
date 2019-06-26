from .config import create_app
from .api import api_blueprint, api
from .controller import ProjectsDataHandler, ProjectsInitializer, ProjectsResources

app = create_app()
app.register_blueprint(api_blueprint, url_prefix="/api")

api.add_resource(ProjectsDataHandler, '/projects/data/<id>')
api.add_resource(ProjectsInitializer, '/projects')
api.add_resource(ProjectsResources, '/projects/<id>')
