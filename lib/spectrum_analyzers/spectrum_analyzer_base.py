import abc

class SpectrumAnalyzerABC(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_spectrum(self):
        raise NotImplementedError('users must define get_spectrum to use this base class')

    @abc.abstractmethod
    def get_freqs(self):
        raise NotImplementedError('users must define get_freqs to use this base class')
