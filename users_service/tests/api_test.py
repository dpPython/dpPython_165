import unittest
from core.app import app
from tests.data_for_test import data_all_users, data_user
import json
# python -m unittest tests.api_test


class FlaskTestApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_all_users(self):
        users = self.app.get('/users/api/users')
        self.assertEqual(users.status_code, 200)

        content = json.loads(users.get_data(as_text=True))
        self.assertEqual(content, data_all_users)

    def test_get_user(self):
        user = self.app.get('/users/api/alice')
        self.assertEqual(user.status_code, 200)

        content = json.loads(user.get_data(as_text=True))
        self.assertEqual(content, data_user)

    def test_get_none_user_404(self):
        user = self.app.get('/users/api/don')
        self.assertEqual(user.status_code, 404)

    '''
    def test_post_user(self):
        post_data = {
            'username': 'nina',
            'password_hash': 'nina',
            'email': 'nina@example.com',
            'user_address': 'Ninskaya,27'
        }
        user = self.app.post('/users/api/users/', data=json.dumps(post_data))
        self.assertEqual(user.status_code, 201)
        self.assertEqual(user.content_type, 'application/json')
    '''

    def test_post_none_user(self):
        user = self.app.post('/users/api/users/', data=None)
        self.assertEqual(user.status_code, 404)

    def test_api_wrong_address(self):
        user = self.app.get('/users/download')
        self.assertEqual(user.status_code, 404)


if __name__ == "__main__":
    unittest.main()
