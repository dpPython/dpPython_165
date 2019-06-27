from flask_restful import Api
from flask import Blueprint


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)