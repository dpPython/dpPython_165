from flask import jsonify, request
from flask_restful import Resource
from Model import db, Rule, Contract, RuleSchema

rules_schema = RuleSchema(many=True)
rule_schema = RuleSchema()


class RuleResource(Resource):
    def get(self):
        rules = Rule.query.all()
        rules = rules_schema.dump(rules).data
        return {"status": "success", "data": rules}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = rule_schema.load(json_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        contract_id = Contract.query.filter_by(id=data['contract_id']).first()
        if not contract_id:
            return {'status': 'error', 'message': 'contract not found'}, 400
        rule = Rule(
            contract_id=data['contract_id'],
            square=data['square'],
            living_square=data['living_square'],
            rooms=data['rooms'],
            toilets=data['toilets']
            )
        db.session.add(rule)
        db.session.commit()

        result = rule_schema.dump(rule).data

        return {'status': "success", 'data': result}, 201
