import os
import pytest
import tempfile

from flaskr import flaskr


@pytest.fixture
def client():
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()

    yield client

