How to create a smart contract
==============================

A smart contract in pyledger is a function that looks pretty much like an object, it has attributes and methods that
change those attributes. It is also quite similar as how Solidity defines the smart contracts, with attributes and
methods that modify them. Pyledger is a little more explicit.

The contract is

The methods get the attributes as the first argument,
in a similar fashion as a method in Python gets the ``self``, but if they modify those attributes, that argument must
be returned.

.. autoclass:: pyledger.contract.Builder
   :members: add_method, add_property
