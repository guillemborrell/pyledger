# Pyledger.

## A simple ledger for smart contracts written in Python

Smart contracts are taking over the financial ecosystem, but most platforms
are terribly complicated given their parallel nature. What happens is that,
if you don't need to deal with parallelism, building a ledger for smart
contracts is relatively easy. Here's where Pyledger comes into play.

Assume that you want to create a smart contract to implement a digital
currency system. You have some features you consider necessary, namely
creating accounts, adding currency to any account, checking the balance and
transfer some amount.

A smart contract is an application, therefore a smart contract is code. In
Pyledger you can implement your smart contract in Python. In a few words, a
smart contract in PyLedger is a function that uses the Builder class

```python
from pyledger.contract import Builder

def ledger():
    def add_account(props, key: str):
        if key in props.accounts:
            raise Exception('Account already exists')

        props.accounts[key] = 0.0
        return props

    def increment(props, key: str, quantity: float):
        if key not in props.accounts:
            raise Exception('Account not found')

        props.accounts[key] += quantity
        return props

    def transfer(props, source: str, dest: str, quantity: float):
        if source not in props.accounts:
            raise Exception('Source account not found')
        if dest not in props.accounts:
            raise Exception('Destination account not found')
        if props.accounts[source] < quantity:
            raise Exception('Not enough funds in source account')

        props.accounts[source] -= quantity
        props.accounts[dest] += quantity

        return props

    def balance(props, key: str):
        if key not in props.accounts:
            print(props.accounts)
            raise Exception('Account not found')

        return props, str(props.accounts[key])

    contract = Builder('DigitalCurrency')
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)
    contract.add_method(transfer)
    contract.add_method(balance)

    return contract
```

There is no need to deal with the details now, but if you are familiar with
Python you more or less understand where the thing is going. Once you have
finished creating your smart contract, PyLedger can get it up and running in
no time as a tornado or wsgi application.

```python
from pyledger.handlers import make_tornado
from pyledger.contract import Builder
from pyledger.config import args
import tornado.ioloop

if __name__ == '__main__':
    application = make_tornado(ledger)
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
```

Assume that the previous script is called *ledger.py*. Running the ledger is
as simple as running the script with some options

```
$> python ledger.py --sync
```

Now you have your ledger up and running, you can connect to it with a REPL
client.

```
$> pyledger-shell
PyLedger simple client
(http://localhost:8888)> help

Documented commands (type help <topic>):
========================================
api  call  contracts  exit  help  key

(http://localhost:8888)> contracts
     DigitalCurrency
(http://localhost:8888)> api DigitalCurrency
   add_account ( key [str] )
   increment ( key [str], quantity [float] )
   transfer ( source [str], dest [str], quantity [float] )
   balance ( key [str] )

(http://localhost:8888)> call DigitalCurrency add_account account1
SUCCESS
(http://localhost:8888)> call DigitalCurrency increment account1 10.0
SUCCESS
(http://localhost:8888)> call DigitalCurrency balance account1
10.0
(http://localhost:8888)> call DigitalCurrency add_account account2
SUCCESS
(http://localhost:8888)> call DigitalCurrency transfer account1 account2 5.0
SUCCESS
(http://localhost:8888)> call DigitalCurrency balance account1
5.0
(http://localhost:8888)> call DigitalCurrency balance account2
5.0
(http://localhost:8888)> exit
```