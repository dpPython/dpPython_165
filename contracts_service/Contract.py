from flask import request
from flask_restful import Resource
from ..model import db, Contract, ContractSchema

contracts_schema = ContractSchema(many=True)
contract_schema = ContractSchema()


class ContractResource(Resource):
    def get(self):
        contracts = Contract.query.all()
        contracts = contracts_schema.dump(contracts).data
        return {'status': 'success', 'data': contracts}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = contract_schema.load(json_data)
        if errors:
            return errors, 422
        contract = Contract.query.filter_by(name=data['name']).first()
        if contract:
            return {'message': 'Contract already exists'}, 400
        contract = Contract(
            name=json_data['name']
            )

        db.session.add(contract)
        db.session.commit()

        result = contract_schema.dump(contract).data

        return {"status": 'success', 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = contract_schema.load(json_data)
        if errors:
            return errors, 422
        contract = Contract.query.filter_by(id=data['id']).first()
        if not contract:
            return {'message': 'Contract does not exist'}, 400
        contract.name = data['name']
        db.session.commit()

        result = contract_schema.dump(contract).data

        return {"status": 'success', 'data': result}, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = contract_schema.load(json_data)
        if errors:
            return errors, 422
        contract = Contract.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = contract_schema.dump(contract).data

        return {"status": 'success', 'data': result}, 204
