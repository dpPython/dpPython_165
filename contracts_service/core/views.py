from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from core.models import db, Rule, RuleSchema, Contract, ContractSchema
from sqlalchemy.exc import SQLAlchemyError
from core import status

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

rule_schema = RuleSchema()
contract_schema = ContractSchema()

class ContractResource(Resource):
    def get(self, id):
        contract = Contract.query.get_or_404(id)
        result = contract_schema.dump(contract).data
        return result

    def patch(self, id):
        contract = Contract.query.get_or_404(id)
        contract_dict = request.get_json(force=True)
        if 'contract_name' in contract_dict:
            contract.contract_name = contract_dict['contract_name']
        # if 'duration' in contract_dict:
        #     contract.duration = contract_dict['duration']
        # if 'printed_times' in contract_dict:
        #     contract.printed_times = contract_dict['printed_times']
        # if 'printed_once' in contract_dict:
        #     contract.printed_once = contract_dict['printed_once']
        dumped_contract, dump_errors = contract_dict.dump(contract)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = contract_schema.validate(dumped_contract)
        # errors = message_schema.validate(data)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            contract.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        contract = Contract.query.get_or_404(id)
        try:
            delete = contract.delete(contract)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class ContractListResource(Resource):
    def get(self):
        contracts = Contract.query.all()
        result = contract_schema.dump(contracts, many=True).data
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = contract_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            rule_name = request_dict['rule']['name']
            rule = Rule.query.filter_by(name=rule_name).first()
            if rule is None:
                # Create a new rule
                rule = Rule(name=rule_name,
                            f_operand = request_dict['f_operand'],
                            s_operand = request_dict['s_operand'],
                            operator = request_dict['operator'],
                            coefficient = request_dict['coefficient'])
                db.session.add(rule)
            # create a new contract
            contract = Contract(
                contract_name=request_dict['contract_name'],
                information=request_dict['information'],
                rule=rule)

            # requests.put('http://0.0.0.0/{port}/projects', jsonify={
            #     "project_name": 'project_name',
            #     "contract_id": UUID,
            #     status: status.HTTP_201_CREATED
            # })

            contract.add(contract)
            query = Contract.query.get(contract.id)
            result = contract_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


class RuleResource(Resource):
    def get(self, id):
        rule = Rule.query.get_or_404(id)
        result = rule_schema.dump(rule).data
        return result

    def patch(self, id):
        rule = Rule.query.get_or_404(id)
        rule_dict = request.get_json()
        if not rule_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = rule_schema.validate(rule_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in rule_dict:
                rule.name = rule_dict['name']
            rule.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        rule = Rule.query.get_or_404(id)
        try:
            rule.delete(rule)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class RuleListResource(Resource):
    def get(self):
        rules = Rule.query.all()
        results = rule_schema.dump(rules, many=True).data
        return results

    def post  (self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = rule_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            rule = Rule(
                name=request_dict['name'],
                f_operand=request_dict['f_operand'],
                s_operand=request_dict['s_operand'],
                operator=request_dict['operator'],
                coefficient=request_dict['coefficient'])
            rule.add(rule)
            query = Rule.query.get(rule.id)
            result = rule_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


api.add_resource(RuleListResource, '/rules/')
api.add_resource(RuleResource, '/rules/<id>')
api.add_resource(ContractListResource, '/')
api.add_resource(ContractResource, '/<id>')
