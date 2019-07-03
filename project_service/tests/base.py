from flask.ext.testing import TestCase

from core.config import db
from core.api import api_api
from core.models import Projects, Data


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(Projects("admin", "ad@min.com", "admin"))
        # db.session.add(
        #     BlogPost("Test post", "This is a test. Only a test.", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
