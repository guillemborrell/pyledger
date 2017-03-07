from collections import namedtuple
import tornado.web
import argparse
import sys


if len(sys.argv) > 2 and 'test' in sys.argv[2]:
    argstype = namedtuple('Arguments', ['db', 'debug', 'sync'])
    args = argstype(db='sqlite://', debug=False, sync=True)

else:
    parser = argparse.ArgumentParser(description='Run the PyLedger server')
    parser.add_argument('--db', help="SQLAlchemy database address",
                        type=str, default="sqlite://")
    parser.add_argument('--sync', action='store_true')
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

        
def make_application():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        db=args.db,
        debug=args.debug)
