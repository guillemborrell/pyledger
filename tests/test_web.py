from tornado.testing import AsyncHTTPTestCase
from pyledger.handlers import make_tornado
from urllib import parse
import json


class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        return make_tornado()

    def test_00get_contracts(self):
        response = self.fetch('/contracts')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'["New contract"]')

    def test_01get_user_key(self):
        response = self.fetch('/new_user')
        self.assertEqual(response.code, 200)
        self.assertEqual(len(response.body), 36)

    def test_02get_api(self):
        response = self.fetch('/api?{}'.format(
            parse.urlencode({'contract': 'New contract'})
        ))
        print(json.loads(response.body))
        self.assertEqual(response.code, 200)
        self.assertEqual(len(response.body), 81)
        
    def test_03call(self):
        response = self.fetch('/call?{}'.format(
            parse.urlencode({'contract': 'New contract',
                             'function': 'add_account',
                             'key': 'My account'})))
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'SUCCESS')
                             
