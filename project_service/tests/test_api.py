import unittest
from core.app import app

# python -m unittest test_api


class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_main(self):
        prj = self.app.get('/projects')
        assert prj.status == '200 OK'
        # assert b'Main' in prj.data
        #assert False

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
