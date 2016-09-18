import utils

import numpy as np


def bin_lims(n, nbins):
    start_indices = (np.arange(nbins) * float(n) / float(nbins)).astype(int)
    return zip(start_indices, np.concatenate((start_indices[1:], [int(n)])))


def bin_fft(freq, nbins):
    n = len(freq)
    bins = np.zeros(nbins)
    for i, lims in enumerate(bin_lims(n, nbins)):
        bins[i] = np.mean(freq[lims[0]:lims[1]])

    return bins


class Visualizer(object):

    def __init__(self, nlights, nbins=3, color=np.array([[255, 0, 0]])):
        self.nlights = nlights
        self.lights = np.zeros((self.nlights, 3)).astype('uint8')

        self.nbins = nbins
        self.color = color
        tiny = 1E-4
        self.maxes = np.zeros(self.nbins) + tiny

    def freq_to_hex(self, freq):
        bin_amplitudes = bin_fft(freq, self.nbins)
        self.maxes = np.max(np.vstack((self.maxes, bin_amplitudes)), axis=0)
        normed_amplitudes = bin_amplitudes / self.maxes

        for i, lims in enumerate(bin_lims(self.nlights, self.nbins)):
            self.lights[lims[0]:lims[1], :] = (
                    self.color * normed_amplitudes[i]).astype(int)

        return map(utils.rgb_to_hex, self.lights)
