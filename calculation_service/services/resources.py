from flask_restful import Resource
from flask import jsonify, request
from .models import Calculation
from .mission import calculate_by_rules
from .config import db
from services.data_api import AccessToProjects


class Calculate(Resource):
    def post(self):

        calculate_by_rules.delay(request.json["project_id"])
        AccessToProjects.put(request.json["project_id"], 'in progress')


class Results(Resource):
    def get(self):
        project_id = request.json["project_id"]
        calculation = db.session.query(Calculation).filter_by(project_id=project_id).first()
        return jsonify({"result": calculation})
