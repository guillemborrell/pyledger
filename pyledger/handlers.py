from pyledger.contract import ls_contracts
from pyledger.config import args
from collections import namedtuple
import tornado.web
import argparse
import sys
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class ContractsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps([c for c in ls_contracts()]))

        
def make_application():
    return tornado.web.Application(
        [
            (r"/contracts", ContractsHandler),
            (r"/", MainHandler),
        ],
        db=args.db,
        debug=args.debug)
