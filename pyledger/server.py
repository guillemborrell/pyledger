from pyledger.handlers import application
import tornado.ioloop

def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

