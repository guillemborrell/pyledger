How to create a smart contract
==============================

A smart contract in pyledger is a function that returns an instance of :py:class:`pyledger.contract.Builder`. This
object is a helper to manage the attributes of the smart contract and the methods that may or may not modify those
attributes. The simplest smart contract you may think of is one that just returns the string "Hello, World".


The methods get the attributes as the first argument in a similar fashion as a method in Python gets the ``self``, and
it

Note that the contract function pretty much looks like an object, it has attributes and methods that
change those attributes. It is also quite similar as how Solidity defines the smart contracts, with attributes and
methods that modify them. Pyledger is a little more explicit.


Docstrings of the classes cited in this section
-----------------------------------------------

.. autoclass:: pyledger.contract.Builder
   :members: add_method, add_property
