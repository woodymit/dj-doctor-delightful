# from spectrum_analyzer_abc import SpectrumAnalyzer
from spectrum_analyzers.spectrum_analyzer_base import SpectrumAnalyzerABC

import librosa
import numpy as np


class WindowedSTFT(SpectrumAnalyzerABC):

    def __init__(self, nsamples, sample_rate, logscale=False):
        self.nsamples = nsamples
        self.win = np.hanning(self.nsamples)
        self.sample_rate = sample_rate
        self.logscale = logscale
        self.freqs = np.arange((nsamples / 2) + 1, dtype=np.int32) / (nsamples / sample_rate)
    
    def get_spectrum(self, x):
        # normalized, windowed frequencies in data chunk
        spec = np.fft.rfft(x * self.win) / self.nsamples

        # get magnitude 
        psd = abs(spec)

        # convert to dB scale
        if self.logscale:
            psd = 20 * np.log10(psd)

        return psd

    def get_freqs(self):
        return self.freqs.copy()


class CQT(SpectrumAnalyzerABC):

    def __init__(self, nsamples, sample_rate, n_octaves=7 , bins_per_octave=12):
        self.nsamples = nsamples
        self.sample_rate = sample_rate
        self.n_octaves = n_octaves
        self.bins_per_octave = bins_per_octave
        self.n_bins = self.n_octaves * self.bins_per_octave
        assert self.nsamples % (2 ** self.n_octaves) == 0

    def get_spectrum(self, x):

        print("len(x):", len(x))
        print("nsamples:", self.nsamples)

        cqt = librosa.core.cqt(x.astype(float), self.sample_rate, hop_length=self.nsamples,
                n_bins=self.n_bins, bins_per_octave=self.bins_per_octave)


        # get magnitude
        cqt = abs(cqt)

        print('cqt.shape:', cqt.shape)

        return cqt[:,0]

    def get_freqs(self):
        assert False



