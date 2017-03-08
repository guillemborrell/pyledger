from pyledger.handlers import make_application
from pyledger.config import args
import tornado.ioloop


def main():
    application = make_application()
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()

