How to create a smart contract
==============================

A smart contract in pyledger is a function that returns an instance of :py:class:`pyledger.contract.Builder`. This
object is a helper to manage the attributes of the smart contract and the methods that may or may not modify those
attributes. The simplest smart contract you may think of is one that just returns the string "Hello".

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

If you run this snippet as script without options, you will be able to connect to this server with the command line
client provided by pyledger, called ``pyledger-shell``::

    (env) guillem@demencia:~/projects/pyledger$ pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> contracts
         Hello
    (http://localhost:8888)> api Hello
       say_hello (  )

    (http://localhost:8888)> call Hello say_hello
    Hello
    (http://localhost:8888)>


The methods get the attributes as the first argument in a similar fashion as a method in Python gets the ``self``, and
it

Note that the contract function pretty much looks like an object, it has attributes and methods that
change those attributes. It is also quite similar as how Solidity defines the smart contracts, with attributes and
methods that modify them. Pyledger is a little more explicit.


Docstrings of the classes cited in this section
-----------------------------------------------

.. autoclass:: pyledger.contract.Builder
   :members: add_method, add_property
