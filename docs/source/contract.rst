How to create a smart contract
==============================

A smart contract in pyledger is a function that returns an instance of
:py:class:`pyledger.contract.Builder`. This object is a helper to manage the
attributes of the smart contract and the methods that may or may not modify
those attributes. The simplest smart contract you may think of is one that
just returns the string "Hello". 

.. code-block:: python

    from pyledger.handlers import make_tornado
    from pyledger.contract import Builder
    from pyledger.config import args
    import tornado.ioloop


    def hello():
        def say_hello(attrs):
            return attrs, 'Hello'

        contract = Builder('Hello')
        contract.add_method(say_hello)

        return contract


    if __name__ == '__main__':
        application = make_tornado(hello)
        application.listen(args.port)
        tornado.ioloop.IOLoop.instance().start()

If you run this snippet as script without options, you will be able to
connect to this server with the command line client provided by pyledger,
called ``pyledger-shell``::

    (env) :~$ pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> contracts
         Hello
    (http://localhost:8888)> api Hello
       say_hello (  )

    (http://localhost:8888)> call Hello say_hello
    Hello
    (http://localhost:8888)>


This almost trival example is useful to understand the very basics about how
the contracts are created. The contract is called *Hello* which is the argument
of the Builder instance. The method *say_hello* gets no arguments and it
modifies no attributes, but it must get the attributes as an argument and
return them anyways.  If an additional argument, like the ``Hello`` string,
is returned by the method, it is given as a second return argument.

Let's change the previous example a little by adding an attribute to the
contract. For instance, we will make a counter of the amount of times the
contract has greeted us.

.. code-block:: python

    def hello():
        def say_hello(attrs):
            attrs.counter += 1
            return attrs, 'Hello {}'.format(attrs.counter)

        contract = Builder('Hello')
        contract.add_attribute('counter', 0)
        contract.add_method(say_hello)

        return contract

A session with this new smart contract would be as follows::

    (http://localhost:8888)> call Hello say_hello
    Hello 1
    (http://localhost:8888)> call Hello say_hello
    Hello 2
    (http://localhost:8888)> status Hello
    {'counter': 2}


Note that the contract function pretty much looks like an object, it has
attributes and methods that change those attributes. It is also quite similar
as how Solidity defines the smart contracts, with attributes and
methods that modify them. Pyledger is a little more explicit.


Docstrings of the classes cited in this section
-----------------------------------------------

.. autoclass:: pyledger.contract.Builder
   :members: add_method, add_attribute
