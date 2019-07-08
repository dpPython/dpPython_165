import unittest
from core.run import app
from core.tests.test_data import all_contracts
import json


class FlaskTestApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_all_contracts(self):
        contracts = self.app.get('/contracts/')
        self.assertEqual(contracts.status_code, 200)

        content = json.loads(contracts.get_data(as_text=True))
        self.assertEqual(content, all_contracts)

    def test_get_contract(self):
        contract = self.app.get('/contracts/bd6e148d-254e-465f-b7bb-5fc7231c358a')
        self.assertEqual(contract.status_code, 200)

        content = json.loads(contract.get_data(as_text=True))
        self.assertEqual(content, contract)

    def test_get_none_contract_404(self):
        contract = self.app.get('/contracts/none_contract')
        self.assertEqual(contract.status_code, 404)

    def test_post_contract(self):
        post_data = {
            "contract_name": "test_name",
            "information": "test_message",
            "rule": "test_rule",
            "f_operand": "field_1",
            "s_operand": "field_2",
            "operator": "+",
            "coefficient": "5.5"
        }
        contract = self.app.post('/contracts/', data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(contract.status_code, 200)
        self.assertEqual(contract.content_type, 'application/json')

    def test_post_none_contract(self):
        contract = self.app.post('/contracts/', data=None)
        self.assertEqual(contract.status_code, 404)

    def test_api_wrong_address(self):
        contract = self.app.get('/contracts/test')
        self.assertEqual(contract.status_code, 404)


if __name__ == "__main__":
    unittest.main()
