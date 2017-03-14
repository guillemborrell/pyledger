The status chain
================

Pyledger does not use a blockchain or any similar protocol because its not
distributed nature makes it very unefficient. The internal storage for every
contract is not divided in blocks, and each state is stored as soon as it is
sent to the server.

One of the important features of the blockchain is that it is impossible for
anyone, even the owner of the data, to tamper with its contents. Pyledger
also has this feature, but in a slightly different fashion. All the statuses
stored in the ledger for every contract are hashed with te previous hash and
the date and time of insertion. This is a kind of *status chain* instead of a
block chain.

All the hashes are secure, using a SHA-256 for which no collision has been
found yet, which is the same as the used by Bitcoin. This means that one can
verify that noone has been tampering with the backend database that stores
the statuses. We can use the *verify* command of the client to check that the
greeter smart contract works as expected::

    (env) $> pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #2
    (http://localhost:8888)> verify Hello
    'Contract OK'

