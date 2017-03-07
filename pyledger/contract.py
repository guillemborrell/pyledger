from collections import namedtuple
from uuid import uuid4
from pyledger.db import DB, Contract, Status
from datetime import datetime
import inspect
import dill


class Builder():
    def __init__(self, name='', obj=None):
        if obj is None: 
            self.attributes = {}
            self.methods = {}
        else:
            raise NotImplemented('Inspecting from class not supported yet')

        if name:
            self.name = name
        else:
            self.name = str(uuid4())

        self.description = ''
    
    def add_description(self, description: str):
        self.description = description

    def add_attribute(self, name: str, value):
        """
        Add attribute *name* to the contract with an initial value of *value*
        """
        self.attributes[name] = value

    def add_method(self, method, name: str=''):
        """
        Add a method to the contract
        """
        if not name:
            name = method.__name__

        sig = inspect.signature(method)

        if 'props' not in sig.parameters:
            raise ValueError(
                'The first argument of the method must be'
                ' called props and not annotated'
            )
        else:
            for param in sig.parameters:
                if not param == 'props' and sig.parameters[param].annotation == inspect._empty:
                    raise ValueError(
                        'Parameter {} without signature'.format(
                            param))
                
        self.methods[name] = method

    def call(self, function: str, **kwargs):
        """
        Call the function of the smart contract passing the keyword arguments.
        """
        # Build named tuple with the properies
        Props = namedtuple('Props', self.attributes.keys())
        props = Props(**self.attributes)
        
        signature = inspect.signature(self.methods[function])
        call_args = {'props': props}

        for k,v in kwargs.items():
            if k in signature.parameters:
                if type(v) == signature.parameters[k].annotation:
                    call_args[k] = v
                else:
                    return 'Parameter {} not of correct type {}'.format(
                        k,
                        signature.parameters[k].annotation
                        )

        try:
            self.methods[function](**call_args)
            self.props = props._asdict()
            return 'SUCCESS'
        except Exception as e:
            return str(e)
        
        
    def api(self):
        """
        Return a dictionary with the complete API for the contract
        """
        api_spec = {}
        for method in self.methods:
            function_spec = {}
            sig = inspect.signature(self.methods[method])
            for param in sig.parameters:
                function_spec[param] = sig.parameters[param].annotation

            api_spec[method] = function_spec

        return (self.name, api_spec)


def commit_contract(contract):
    """
    Commits the contract to the ledger
    """
    stored_contract = Contract()
    stored_contract.name = contract.name
    stored_contract.created = datetime.now()
    stored_contract.description = contract.description
    stored_contract.methods = dill.dumps(contract.methods)

    first_status = Status()
    first_status.contract = stored_contract
    first_status.when = datetime.now()
    first_status.attributes = dill.dumps(contract.attributes)

    DB.session.add(stored_contract)
    DB.session.add(first_status)
    DB.session.commit()

def ls_contracts():
    """
    Get the name of all the contracts
    """
    for contract in DB.session.query(Contract).order_by(Contract.created):
        yield contract.name
