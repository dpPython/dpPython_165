from flask import jsonify
from flask_restful import Resource
from .models import Calculation


class Calculate(Resource):
    def post(self):
        # input correct url to get an info about contract
        contract = self.get("contract_id")
        project = contract.get("project_id")
        rules = contract.get("rules")
        data = self
        cost = data.get("price").get("currency_value")
        result = 0
        for key in data:
            if key in rules:
                result += (data.get(key) * rules.get(key) * cost)

        currency = data.get('price').get('currency')
        result = '{:.3f} '.format(result) + currency
        request.put('/status', 'completed')
        return result

    def get(self):
        return Calculation.result
