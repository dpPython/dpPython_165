from flask import Blueprint
from flask_restful import Api

bp = Blueprint('users', __name__)
usr_api = Api(bp)
