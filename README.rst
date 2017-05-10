Pyledger
========

**A simple ledger for smart contracts written in Python**

.. image:: https://badge.fury.io/py/pyledger.svg
    :target: https://badge.fury.io/py/pyledger

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
    :target: https://pyledger.readthedocs.io/en/latest

.. image:: https://badge.fury.io/gh/guillemborrell%2Fpyledger.svg
    :target: https://badge.fury.io/gh/guillemborrell%2Fpyledger

Smart contracts are taking over the financial ecosystem, but most platforms
are terribly complicated given their parallel nature. What happens is that,
if you don't need to deal with parallelism, building a ledger for smart
contracts is relatively easy. Here's where Pyledger comes into play.

Assume that you want to create a smart contract to implement a digital
currency system. You have some features you consider necessary, namely
creating accounts, adding currency to any account, checking the balance and
transfer some amount.

A smart contract is an application, so you need to code to create one. In
Pyledger you can implement your smart contract in Python. In a few words, a
smart contract in Pyledger is a Python class

.. code-block:: python

    from pyledger.server.contract import SimpleContract

    class DigitalCurrency(SimpleContract):
        accounts = {}

        def add_account(self, key: str):
            if key in self.accounts:
                raise Exception('Account already exists')

            self.accounts[key] = 0.0
            return key

        def increment(self, key: str, quantity: float):
            if key not in self.accounts:
                raise Exception('Account not found')

            self.accounts[key] += quantity

        def transfer(self, source: str, dest: str, quantity: float):
            if source not in self.accounts:
                raise Exception('Source account not found')
            if dest not in self.accounts:
                raise Exception('Destination account not found')
            if self.accounts[source] < quantity:
                raise Exception('Not enough funds in source account')
            if quantity < 0:
                raise Exception('You cannot transfer negative currency')

            self.accounts[source] -= quantity
            self.accounts[dest] += quantity

        def balance(self, key: str):
            if key not in self.accounts:
                print(self.accounts)
                raise Exception('Account not found')

            return str(self.accounts[key])


There is no need to deal with the details now, but if you are familiar with
Python you more or less understand where the thing is going. Once you have
finished creating your smart contract, PyLedger can get it up and running in
no time.

.. code-block:: python

    from pyledger.server import run

    run(DigitalCurrency)

Assume that the previous script is called *ledger.py*. Running the ledger is
as simple as running the script with some options::

    $> python ledger.py --sync

Now you have your ledger up and running, you can connect to it with a REPL
client::

    $> pyledger-shell

    Connected to server: tcp:127.0.0.1:9000
    Pyledger REPL client, write 'help' for help or 'help command' for help on a specific command
    PL >>> help

    The Pyledger REPL is a console to interact with a Pyledger server.
    The list of available commands is the following

     help          Shows this help
     disconnect    Disconnects from the server in a clean way.
     contracts     Lists the available contracts in the server
     api           Shows the api for a particular contract
     call          Calls a method of a contract
     broadcast     Broadcast message all clients

    This client may have some limitations respect to a custom client.
    For instance, the server may push notifications to the clients,
    and using the client API, you could define callbacks to those
    pushed messages.

    Read the full documentation in http://pyledger.readthedocs.io

    PL >>> contracts
    ['DigitalCurrency']
    PL >>> api DigitalCurrency
    {'add_account': {'key': <class 'str'>},
     'balance': {'key': <class 'str'>},
     'increment': {'key': <class 'str'>, 'quantity': <class 'float'>},
     'transfer': {'dest': <class 'str'>,
                  'quantity': <class 'float'>,
                  'source': <class 'str'>}}
    PL >>> call DigitalCurrency add_account account1
    Call with pairs of key value arguments
    PL >>> call DigitalCurrency add_account key account1
    'account1'
    PL >>> call DigitalCurrency increment key account1 quantity 100.0
    None
    PL >>> call DigitalCurrency balance key account1
    '100.0'
    PL >>> call DigitalCurrency add_account key account2
    'account2'
    PL >>> call DigitalCurrency transfer source account1 dest account2 quantity 50.0
    None
    PL >>> call DigitalCurrency balance key account1
    '50.0'
    PL >>> call DigitalCurrency balance key account2
    '50.0'
    PL >>> disconnect
    Successfully closed, you can kill this with Ctrl-C
    WebSocket connection closed: 1000; None
    ^CBye


Pyledger is possible thanks to `Autobahn <http://crossbar.io/autobahn/>`_
