from flask import Blueprint
from flask_restful import Api

from .resources import UploadCsv

api_1_0_blueprint = Blueprint('api_1_0', __name__)
api_1_0 = Api(api_1_0_blueprint)

api_1_0.add_resource(UploadCsv, '/upload', endpoint='upload_file')
