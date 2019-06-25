import os
import unittest
from io import BytesIO

from flask import url_for

from app.config import create_app, BASE_DIR

fixture_csv = os.path.join(BASE_DIR, 'fixtures/dataJun-16-2019.csv')


class FlaskClientCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_invalid_get_method_request(self):
        with self.app.test_request_context():
            response = self.client.get(url_for('api_1_0.upload_file'))
            return self.assertEqual(response.status_code, 405)

    def test_invalid_put_method_request(self):
        with self.app.test_request_context():
            response = self.client.put(url_for('api_1_0.upload_file'))
            return self.assertEqual(response.status_code, 405)

    def test_bad_post_method_request(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('api_1_0.upload_file'))
            return self.assertEqual(response.status_code, 400)

    def test_valid_post_method_request(self):
        with self.app.test_request_context():
            response = self.client.post(
                url_for('api_1_0.upload_file'),
                content_type='multipart/form-data',
                data={'file': (BytesIO(b"abcdef"), fixture_csv)})
            return self.assertEqual(response.status_code, 400)
