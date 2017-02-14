# from spectrum_analyzer_abc import SpectrumAnalyzer
from spectrum_analyzers.spectrum_analyzer_base import SpectrumAnalyzerABC

import numpy as np


class WindowedSTFT(SpectrumAnalyzerABC):

    def __init__(self, nsamples, sample_rate):
        self.nsamples = nsamples
        self.win = np.hanning(self.nsamples)
        self.sample_rate = sample_rate
        self.freqs = np.arange((int(nsamples / 2) + 1) / (nsamples / sample_rate))
    
    def get_spectrum(self, x):
        # normalized, windowed frequencies in data chunk
        spec = np.fft.rfft(x * self.win) / self.nsamples

        # get magnitude 
        psd = abs(spec)

        # convert to dB scale
        psd = 20 * np.log10(psd)

        return psd

    def get_freqs(self):
        return self.freqs
