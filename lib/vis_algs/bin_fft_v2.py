import utils

import numpy as np


def bin_lims(n, nbins):
    start_indices = (np.arange(nbins) * float(n) / float(nbins)).astype(int)
    return zip(start_indices, np.concatenate((start_indices[1:], [int(n)])))


def bin_fft(freq, nbins):
    n = len(freq)
    bins = np.zeros(nbins)
    for i, lims in enumerate(bin_lims(n, nbins)):
        bins[i] = np.max(freq[lims[0]:lims[1]])

    return bins


def convex_poly_ramp(x, d=2):
    return -(x - 1) ** 2 + 1


class Visualizer(object):

    def __init__(self, nlights, nbins=90, color=np.array([[255, 0, 0]])):
        self.nlights = nlights
        self.lights = np.zeros(self.nlights)


        self.nbins = nbins
        self.color = color
        tiny = 1E-4
        self.maxes = np.zeros(self.nbins) + tiny



    def freq_to_hex(self, freq):
        bin_amplitudes = bin_fft(freq, self.nbins)
        self.maxes = np.max(np.vstack((self.maxes, bin_amplitudes)), axis=0)
        normed_amplitudes = bin_amplitudes / self.maxes

        # for i, lims in enumerate(bin_lims(self.nlights, self.nbins)):
        #     self.lights[lims[0]:lims[1]] = utils.hsv_to_hex(
        #             float(i) / self.nlights,
        #             1.0,
        #             normed_amplitudes[i])
        # lights_hex = map(utils.rgb_to_hex, self.lights)

        final_hex_vals = []
        for i in range(self.nlights):

            bin_idx = i / self.nlights * int(self.nbins)

            hue = float(i) / self.nlights
            sat = 1.0
            val = convex_poly_ramp(
                    normed_amplitudes[bin_idx], d=4)

            final_hex_vals.append(utils.hsv_to_hex(hue, sat, val))

        return final_hex_vals
