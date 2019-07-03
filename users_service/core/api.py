from flask import Blueprint
from flask_restful import Api
from core.controller import UsersPutGet, UsersPostGet
from manage import app

bp = Blueprint('users', __name__)
#app.register_blueprint(bp, url_prefix='/users')
usr_api = Api(bp)

usr_api.add_resource(UsersPostGet, '/api/users')
usr_api.add_resource(UsersPutGet, '/api/<username>')


# http GET http://localhost:5000/users/api/alice
# http GET http://localhost:5000/users/api/users
# http POST http://localhost:5000/users/api/users username=alice password_hash=dog email=alice@example.com user_address=Pushkina,27
# http PUT http://localhost:5000/users/api/alice email=kolya@example.com
