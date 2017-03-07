from pyledger.handlers import make_application
import tornado.ioloop

def main():
    application = make_application()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

