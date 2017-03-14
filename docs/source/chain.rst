The status chain
================

Pyledger does not use a blockchain or any similar protocol because it would
be very unefficient. The internal storage for every contract is not divided
in blocks, since each state is stored as a register in a SQL database.

One of the important features of the blockchain is that it is impossible for
anyone, even the owner of the data, to tamper with its contents. Pyledger
also has this feature, but in a slightly different fashion. All the statuses
stored in the ledger for every contract are hashed with the
hash of the previous state and the date and time of insertion. It is
therefore impossible to modify a register of the database without leaving
an obvious footprint on the sequence of hashes. This is a kind
of *status chain* instead of a block chain.

All the hashes are secure, since pyledger uses SHA-256, the same as in
Bitcoin. This means that one can
verify that anyone hasn't been tampering with the backend database that stores
the statuses. We can use the *verify* command of the client to check that the
greeter smart contract works as expected::

    (env) $> pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #2
    (http://localhost:8888)> verify Hello
    'Contract OK'

