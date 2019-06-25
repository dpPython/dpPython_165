from flask import Blueprint
from flask_restful import Api
from api.controller import UsersGet, UsersPost, UsersPut, UsersGetAll

bp = Blueprint('api', __name__)

# from api import errors
usr_api = Api(bp)

usr_api.add_resource(UsersGetAll, '/users')
usr_api.add_resource(UsersGet, '/users/<username>')
usr_api.add_resource(UsersPut, '/users/<username>')
usr_api.add_resource(UsersPost, '/users')

# http GET http://localhost:5000/api/users/alice
# http GET http://localhost:5000/api/users
# http POST http://localhost:5000/api/users username=alice password_hash=dog email=alice@example.com address=Pushkina,27
# http PUT http://localhost:5000/api/users/alice email=kolya@example.com
