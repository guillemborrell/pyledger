from pyledger.handlers import make_tornado
from pyledger.contract import Builder
from pyledger.config import args
import tornado.ioloop


def ledger():
    def add_account(props, key: str):
        props.accounts[key] = 0
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
            raise Exception('Account not found')

        return props, props.accounts[key]

    contract = Builder('Digital Currency')
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)
    contract.add_method(transfer)
    contract.add_method(balance)

    return contract

if __name__ == '__main__':
    application = make_tornado(ledger)
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
