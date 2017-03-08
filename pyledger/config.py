import sys
import argparse
from collections import namedtuple


if len(sys.argv) > 2 and 'test' in sys.argv[2]:
    argstype = namedtuple('Arguments', ['db', 'debug', 'sync', 'port'])
    args = argstype(db='sqlite://', debug=False, sync=True, port=8888)

else:
    parser = argparse.ArgumentParser(description='Run the PyLedger server')
    parser.add_argument('--db', help="SQLAlchemy database address",
                        type=str, default="sqlite://")
    parser.add_argument('--sync', action='store_true')
    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('--port', type=int, default=8888)
    args = parser.parse_args()
