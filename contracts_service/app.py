from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Contract import ContractResource
from resources.Rule import RuleResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes

api.add_resource(Hello, '/hello')
api.add_resource(ContractResource, '/contract')
api.add_resource(RuleResource, '/rule')
