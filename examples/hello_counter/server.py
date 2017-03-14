#    Pyledger. A simple ledger for smart contracts implemented in Python
#    Copyright (C) 2017  Guillem Borrell Nogueras
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyledger.handlers import make_tornado
from pyledger.contract import Builder
from pyledger.config import args
import tornado.ioloop


def hello():
    def say_hello(attrs):
        attrs.counter += 1
        return attrs, 'Hello {}'.format(attrs.counter)

    contract = Builder('Hello')
    contract.add_attribute('counter', 0)
    contract.add_method(say_hello)

    return contract


if __name__ == '__main__':
    application = make_tornado(hello)
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
