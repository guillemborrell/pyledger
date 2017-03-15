The status chain
================

Pyledger does not use a blockchain or any similar protocol because it would
be very inefficient for a tool that is not distributed. The internal storage
for every contract is not divided in blocks, since each state is stored as a
register in a SQL database.

One of the important features of the blockchain is that it is impossible for
anyone, even the owner of the data, to tamper with its contents. Pyledger
also has this feature, but in a slightly different fashion. All the statuses
stored in the ledger for every contract are hashed with the the previous
state's hash and the date and time of insertion. It is
therefore impossible to modify a register of the database without leaving
an obvious footprint on the sequence of hashes. This is a kind
of *status chain* instead of a block chain.

All the hashes are secure, since pyledger uses SHA-256, the same as in
Bitcoin. This means that one can verify that anyone hasn't been tampering
with the backend database that stores the statuses. We can use the *verify*
command of the client to check that the greeter smart contract works as
expected. We will start an example session to understand some of the features
of this *status chain* with one of the previous examples::

    (env) $> pyledger-shell
    PyLedger simple client
    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #1
    (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #2
        (http://localhost:8888)> call Hello say_hello Guillem
    Hello Guillem for time #3
    (http://localhost:8888)> status Hello
    {'counter': 3}
    (http://localhost:8888)> verify Hello
    'Contract OK'

The *status* command checks and prints the last status of the contract
attributes, while the *verify* command verifies **at the server side** that
all the statuses of the attributes are consistent. If any of the statuses
is inconsistent with the chain, that inconsistency and its timestamp will be
printed.

Of course, you may not trust the server-side operations on the *status
chain*, which is quite smart. For that reason you can dump all the statuses
of the contract with their corresponding signatures and timestamps with the
following command::

    (http://localhost:8888)> status Hello dump ./hello-ledger.json
    Contract data dump at ./hello-ledger.json
    (http://localhost:8888)> exit

The dumped file looks like this::

    [{'attributes': 'gAN9cQBYBwAAAGNvdW50ZXJxAUsAcy4=',
      'hash': 'Z2VuZXNpcw==',
      'when': '2017-03-15T18:24:27.523828'},
     {'attributes': 'gAN9cQBYBwAAAGNvdW50ZXJxAUsBcy4=',
      'hash': 'eRs+YxhvKIyUdl++TQZ5sCcMDE0aoaNKn1swFQ44bMM=',
      'when': '2017-03-15T18:24:38.846864'},
     {'attributes': 'gAN9cQBYBwAAAGNvdW50ZXJxAUsCcy4=',
      'hash': 'ZGELWR6y7n+hneBbR+8x9PwaRpBi3Bi0CI/T+9J7ccY=',
      'when': '2017-03-15T18:24:39.580593'},
     {'attributes': 'gAN9cQBYBwAAAGNvdW50ZXJxAUsDcy4=',
      'hash': '7B+OH/4xxJz6J6NOixl32F1vXrWZFNQKMR7pe/HO7gY=',
      'when': '2017-03-15T18:24:39.925244'}]

Every state has three properties. The first one is the hash, which is a
base64-encoded SHA-526 hash; the second one is the timestamp of the addition to
the database in the ISO 8601 format, while the third are all the attributes
of the contract, also properly serialized.

.. note::

   If you want to deserialize the attributes to look inside that funny
   string, they are pickled and then base64 encoded

If you want to verify the dumped statuses of the contract you can use the
utility *pyledger-verify*::

    $> pyledger-verify --data hello-ledger.json
    ...
    DONE

where every dot is one successfully verified step.