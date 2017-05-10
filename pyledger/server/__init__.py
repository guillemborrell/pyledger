from pyledger.server.config import args as cmd_args
from pyledger.server.db import DB
from pyledger.server.contract import register_contract
from pyledger.server.ws import run_server


def run(*args, address="ws://127.0.0.1:9000"):
    """
    Make Pyledger server with the given contracts as classes

    :param args: Contract classes
    :param address: Address to bind the websocket server. Defaults to ws://127.0.0.1:9000
    :return:
    """
    if cmd_args.sync:
        DB.sync_tables()

    for contract in args:
        register_contract(contract())

    run_server(address=address)
