from constants import (
        MIN_BUCKET, MAX_BUCKET, NUM_LIGHTS, MAX_AMPLITUDE, BASS_MAX_FREQ)
import utils

import numpy as np


class Visualizer(object):

    def __init__(self, nlights, nbins=3, color=np.array([[255, 0, 0]])):
        self.nlights = nlights
        self.lights = np.zeros((self.nlights, 3))

        self.nbins = nbins
        self.color = color
        tiny = 1E-4
        self.maxes = np.zeros(self.nbins) + tiny

    def freq_to_hex(self, freq):
        num_buckets = len(freq)
        light_amplitude_values = np.zeros(self.nlights)
        for i in range(num_buckets):
            # populate light_amplitude_values with the result from the fft.
            for j in range(
                    int(float(i) * self.nlights / num_buckets),
                    int(float(i + 1) * self.nlights / num_buckets)):
                light_amplitude_values[j] = freq[i]

        final_hex_vals = np.chararray(self.nlights, itemsize=7)
        for i in range(self.nlights):
            final_hex_vals[i] = utils.hsv_to_hex_rgb_str(
                    float(i) / self.nlights, 1.0,
                    light_amplitude_values[i] * 1.0 / MAX_AMPLITUDE)

        return final_hex_vals
