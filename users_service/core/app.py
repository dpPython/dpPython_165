from .api import usr_api, bp
from .config import create_app
from .controller import UsersPutGet, UsersPostGet

app = create_app()
app.register_blueprint(bp, url_prefix='/users')

usr_api.add_resource(UsersPostGet, '/api/users')
usr_api.add_resource(UsersPutGet, '/api/<username>')
