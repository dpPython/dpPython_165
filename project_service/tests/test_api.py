import unittest

import json
from core.app import app

# python -m unittest test_api to run tests


class TestMyAppCRUD(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_getting_all_projects(self):
        # HTTP GET request to the application on certain path
        prj = self.app.get('/projects')

        # assert the status code and type of response
        self.assertEqual(prj.status_code, 200)
        self.assertNotEqual(prj.status_code, 400)
        self.assertEqual(prj.content_type, 'application/json')

    # Test data:
    data = {
        'status': 'create_schema',
        'name': 'project',
        'contract_id': '18f441a0-d0b1-4b22-b16b-c1e718dab64d'
    }

    def test_getting_certain_project(self, _id='35f7a772-fa26-4c7e-91a5-969b1c635ac3'):
        # HTTP GET request to the application on certain path
        prj = self.app.get('/projects/{}'.format(_id), data=json.dumps(self.data), content_type='application/json')

        # assert the status code
        self.assertEqual(prj.status_code, 200)

    def test_getting_certain_project_denial(self, _id='00000000-0000-0000-0000-000000000000'):
        # HTTP GET request with incorrect id
        prj = self.app.get('/projects/{}'.format(_id))
        self.assertEqual(prj.status_code, 404)

    def test_putting_certain_project(self, _id='35f7a772-fa26-4c7e-91a5-969b1c635ac3'):
        # HTTP PUT request to the application on certain path
        prj = self.app.put('/projects/{}'.format(_id))

        # assert the status code
        # self.assertEqual(prj.status_code, 200)
        self.assertEqual(prj.data, b'{"status": "updated"}\n')

    def test_deleting_certain_project(self, _id='35f7a772-fa26-4c7e-91a5-969b1c635ac2'):
        # HTTP DELETE request to the application on certain path
        prj = self.app.delete('/projects/{}'.format(_id))

        # assert the status code
        # self.assertEqual(prj.status_code, 200)
        self.assertEqual(prj.data, b'{"status": "deleted successfully"}\n')

    def test_changing__certain_project_status(self, _id='35f7a772-fa26-4c7e-91a5-969b1c635ac2'):
        # HTTP PUT request to the application on certain path
        prj = self.app.put('/projects/{0}{1}'.format(_id, '/status'))

        # assert the status code
        # self.assertEqual(prj.status_code, 200)
        self.assertEqual(prj.data, b'{"status": "status_updated_successfully"}\n')
