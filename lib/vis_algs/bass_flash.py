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
        num_buckets = freq.size
        bucket_width = (MAX_BUCKET - MIN_BUCKET) * 1.0 / num_buckets
        bass_freq_diff = BASS_MAX_FREQ - MIN_BUCKET
        num_bass_buckets = (int)((bass_freq_diff) * 1.0 / bucket_width)
        all_bass_buckets = freq[0:num_bass_buckets]
        max_bass_val = np.amax(all_bass_buckets)
        all_non_bass_buckets = freq[num_bass_buckets:]
        max_non_bass_index = np.argmax(all_non_bass_buckets)
        hue_value = max_non_bass_index * 1.0 / (num_buckets - num_bass_buckets)
        val_value = max_bass_val * 1.0 / MAX_AMPLITUDE
        hex_representation = utils.hsv_to_hex_rgb_str(
                hue_value, 1.0, val_value)
        final_hex_vals = np.chararray(NUM_LIGHTS, itemsize=7)
        for i in range(NUM_LIGHTS):
            final_hex_vals[i] = hex_representation
        return final_hex_vals
