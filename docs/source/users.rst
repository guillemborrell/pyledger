Users and permissions
=====================

Pyledger supports basic key-based authentication for clients, and the
contracts may be aware if the user was previously created by the administrator
of the ledger. When you run the server for the first time, the ledger server
outputs an admin authentication key, that is stored within the ledger itself::

    $> python examples/authentication/server.py --sync
    Warning: Syncing database at sqlite://
    Warning: Admin key is a1ee413e-0505-49a6-9902-748e87741225

If you start a client with this key, it will have admin privileges.

One of the important aspects of admin privileges is the key creation,
which is equivalent of creating a user, since each user is identified by a
random key::

    $> pyledger-shell --user a1ee413e-0505-49a6-9902-748e87741225
    PyLedger simple client
    (http://localhost:8888)> key NewUser
    Created user Guillem: 79ab6f2d-5fe6-4bf8-9ebd-ee359d9dfa94
    (http://localhost:8888)> exit

This key can be used to authenticate the user, and we can make the contract
aware of the authentication of a client.


.. code-block:: python

    def hello():
        def say_hello(attrs):
            if attrs.user:
                return attrs, 'Hello {}, your key is {}'.format(attrs.user.name,
                                                                attrs.user.key)
            else:
                raise Exception('Not authenticated')

        contract = Builder('Hello')
        contract.add_method(say_hello)

        return contract

The attrs object contains a copy of the data stored about the user, like its
name or the user key. If the user was not authenticated, ``attrs.user`` is
set as ``None``.

We can now start the client with the new user key::

    $> pyledger-shell --user 79ab6f2d-5fe6-4bf8-9ebd-ee359d9dfa94
    (http://localhost:8888)> api Hello
       say_hello (  )

    (http://localhost:8888)> call Hello say_hello
    Hello Guillem, your key is 79ab6f2d-5fe6-4bf8-9ebd-ee359d9dfa94
    (http://localhost:8888)> exit


.. important::

    There is only one user called ``admin``, that is assigned the key that is
    printed when the ledger is started for the first time with the ``--sync``
    option. This means that, ``if attrs.user.name == 'admin'`` checks if the
    current user is in fact the owner of the ledger.

