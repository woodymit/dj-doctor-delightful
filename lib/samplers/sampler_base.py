import abc

class SamplerABC(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read_chunk(self):
        raise NotImplementedError('users must define get_spectrum to use this base class')

    def close(self):
        pass
