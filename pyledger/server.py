"""
This is an example server so you can use it as a template.
"""
from pyledger.handlers import make_tornado
from pyledger.config import args
import tornado.ioloop


def main():
    application = make_tornado()
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()

