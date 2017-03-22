Distributed ledger with the RAFT consensus protocol
===================================================

While having a unique and centralized database allows pyledger to significantly
simplify the ledger infrastructure, it becomes a single point of failure.
However, since the database is a pluggable component in pyledger, you can turn
pyledger into a distributed ledger using a distributed database.

One interesting choice is `rqlite <https://github.com/rqlite/rqlite>`_, a
distributed and relational database built on SQLite where all the nodes reach
a consensus based on the RAFT protocol.

To integrate rqlite with pyledger you must install the packages
sqlalchemy_rqlite and pyrqlite, and run pyledger with the following arguments::

    python examples/currency_auth/server.py --db rqlite+pyrqlite://localhost:4001/ --sync --debug

