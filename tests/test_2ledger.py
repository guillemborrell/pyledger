from tornado.testing import AsyncHTTPTestCase
from pyledger.handlers import make_tornado
from pyledger.contract import Builder
from urllib import parse
import json


def ledger():
    def add_account(props, key: str):
        props.accounts[key] = 0
        return props

    def increment(props, key: str, quantity: float):
        props.accounts[key] += quantity
        return props

    contract = Builder('Another contract')
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)

    return contract


class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        return make_tornado(ledger)

    def test_00get_contracts(self):
        response = self.fetch('/contracts')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'["New contract", "Another contract"]')

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