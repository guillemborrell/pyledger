import abc
import pickle


class Status(abc.ABC):
    """
    Status abstract class
    """
    @abc.abstractmethod
    def __setattr__(self, key: str, value):
        pass

    @abc.abstractmethod
    def __getattr__(self, item: str):
        pass

    @abc.abstractmethod
    def dump(self):
        pass

    @abc.abstractmethod
    def load(self, dump: bytes):
        pass


class SimpleStatus(Status):
    """
    Simple status for the smart contract based on a dictionary.
    """
    def __init__(self, **kwargs):
        self.__dict__['attributes'] = kwargs

    def __setattr__(self, key: str, value):
        self.__dict__['attributes'][key] = value

    def __getattr__(self, item: str):
        return self.__dict__['attributes'][item]

    def dump(self):
        return pickle.dumps(self.__dict__['attributes'])

    def load(self, dump: bytes):
        self.__dict__['attributes'] = pickle.loads(dump)

    def __contains__(self, item):
        return item in self.__dict__['attributes']


Status.register(SimpleStatus)
