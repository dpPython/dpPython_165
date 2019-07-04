from flask_restful import Resource
from flask import jsonify
from .models import Calculation
import services.tasks as tasks
from .config import db


class Calculate(Resource):
    def post(self, project_id):
        tasks.calculate_by_rules.delay(project_id)


class Results(Resource):
    def get(self, id):
        project_id = id.get("project_id")
        calculation = db.session.query(Calculation).filter_by(project_id=project_id).first()
        return jsonify({"result":calculation})
