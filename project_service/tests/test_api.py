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

        # assert the response data
        # self.assertEqual(prj.data, b'{"message": "There are no projects"}\n')

    # Test data:
    data = {
        'status': 'create_schema',
        'name': 'eugene',
        'contract_id': '18f441a0-d0b1-4b22-b16b-c1e718dab64d'
    }

    # def test_posting_project(self):
    #     # HTTP POST request
    #     prj = self.app.post('/projects', data=json.dumps(self.data), content_type='application/json')
    #     self.assertEqual(prj.status_code, 201)

    def test_posting_projects_denial(self):
        # HTTP POST request with no data
        prj = self.app.post('/projects', data=None)
        self.assertEqual(prj.status_code, 400)

    # def test_getting_certain_project(self, _id='862d8628-29c6-48c0-9303-8bfec1c98d56'):
    #     # HTTP GET request to the application on certain path
    #     prj = self.app.get('/projects/{}'.format(_id))
    #
    #     # assert the status code
    #     self.assertEqual(prj.status_code, 200)

    def test_getting_certain_project_denial(self, _id='00000000-0000-0000-0000-000000000000'):
        # HTTP GET request with incorrect id
        prj = self.app.get('/projects/{}'.format(_id))
        self.assertEqual(prj.status_code, 404)

    # def test_putting_certain_project(self, _id='862d8628-29c6-48c0-9303-8bfec1c98d56'):
    #     # HTTP PUT request to the application on certain path
    #     prj = self.app.put('/projects/{}'.format(_id))
    #
    #     # assert the status code
    #     self.assertEqual(prj.status_code, 200)

    def test_putting_certain_project_denial(self, _id='00000000-0000-0000-0000-000000000000'):
        # HTTP PUT request with incorrect id
        prj = self.app.put('/projects/{}'.format(_id))
        self.assertEqual(prj.status_code, 400)

    #     # assert the status code and type of response
    #     self.assertEqual(prj.status_code, 200)
    #     self.assertNotEqual(prj.status_code, 400)
    #
    #     # assert the response data
    #     self.assertEqual(prj.data, b'{"message": "There are no projects"}\n')

    # def test_add(self):
    #     rv = self.app.get('/add/2/3')
    #     self.assertEqual(rv.status, '200 OK')
    #     self.assertEqual(rv.data, '5')
    #
    #     rv = self.app.get('/add/0/10')
    #     self.assertEqual(rv.status, '200 OK')
    #     self.assertEqual(rv.data, '10')
    #
    # def test_404(self):
    #     rv = self.app.get('/other')
    #     self.assertEqual(rv.status, '404 NOT FOUND')
