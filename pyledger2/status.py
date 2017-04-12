import abc
import pickle


class Status(abc.ABC):
    """
    Prototype of status
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
    def __init__(self, **kwargs):
        self.attributes = kwargs

    def __setattr__(self, key: str, value):
        self.attributes[key] = value

    def __getattr__(self, item: str):
        return self.attributes[item]

    def dump(self):
        return pickle.dumps(self.attributes)

    def load(self, dump: bytes):
        self.attributes = pickle.loads(dump)


Status.register(SimpleStatus)
