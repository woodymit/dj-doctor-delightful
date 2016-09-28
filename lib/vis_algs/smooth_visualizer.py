import numpy as np

from vis_algs import smoothing_utils
import utils


def convex_poly_ramp(x, d=2):
    return -(x - 1) ** 2 + 1


class Visualizer(object):

    def __init__(self, nlights):
        self.nlights = nlights

        tiny = 1E-4
        self.maxes = np.zeros(self.nlights) + tiny

    def freq_to_hex(self, freq):

        freq_range = [0, 500]
        sigma = 8

        amplitudes_gauss = smoothing_utils.gaussian_smooth(
                freq, freq_range, self.nlights, sigma)

        assert len(amplitudes_gauss) == self.nlights

        self.maxes = np.max(np.vstack((self.maxes, amplitudes_gauss)), axis=0)
        normed_amplitudes = amplitudes_gauss / self.maxes

        assert all(not np.isnan(a) for a in amplitudes_gauss)

        final_hex_vals = []
        for i in range(self.nlights):

            hue = float(i) / self.nlights
            sat = 1.0
            val = convex_poly_ramp(
                    normed_amplitudes[i], d=4)

            final_hex_vals.append(utils.hsv_to_hex(hue, sat, val))

        return final_hex_vals
