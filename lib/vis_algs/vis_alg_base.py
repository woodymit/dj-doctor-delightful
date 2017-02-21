import abc
import time

import numpy as np

class VisualizationAlgorithmABC(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def freq_to_hex(self, freq):
        pass


class VisualizationAlgorithm(VisualizationAlgorithmABC):

    def __init__(self, nlights):
        self.nlights = nlights
        self.lights = np.zeros((self.nlights, 3))
        self.maxes = None
        self.times = []

    def norm_amplitudes(self, a):

        if self.maxes is None:
            self.maxes = a + 1E-4
            return np.ones(len(a))
        else:
            self.maxes = np.max(np.vstack((self.maxes, a)), axis=0)
            return a / self.maxes

    def log_time(self):
        t = time.clock()
        self.times.append(t)
