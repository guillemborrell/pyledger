import abc
import pickle


class BaseStatus(abc.ABC):
    """
    Status abstract class
    """
    @abc.abstractmethod
    def dump(self):
        pass

    @abc.abstractmethod
    def load(self, dump: bytes):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass


class SimpleStatus(BaseStatus):
    """
    Simple status for the smart contract based on a dictionary.
    """
    def __init__(self, **kwargs):
        self.args_list = [a for a in kwargs]

        for k, v in kwargs.items():
            setattr(self, k, v)

    def dump(self):
        return pickle.dumps({k: getattr(self, k) for k in self.args_list})

    def load(self, dump: bytes):
        status = pickle.loads(dump)
        self.args_list = [a for a in status]

        for k, v in status.items():
            setattr(self, k, v)

    def to_dict(self):
        return {k: getattr(self, k) for k in self.args_list}

    def __contains__(self, item):
        return item in self.__dict__

    def __repr__(self):
        return 'Pyledger status with attributes {}'.format(
            self.args_list)


BaseStatus.register(SimpleStatus)
