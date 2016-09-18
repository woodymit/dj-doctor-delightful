
import numpy as np
import colorsys


MIN_BUCKET = 0  # hz
MAX_BUCKET = 1000  # hz
NUM_LIGHTS = 14  # number of lights around the room
MAX_AMPLITUDE = 1
BASS_MAX_FREQ = 256


# rgb_val is between 0 and 255
def val_to_hex_str(rgb_val):
    representation = ((str)(hex(rgb_val)))[2:]
    if (len(representation) == 1):
        representation = "0" + representation
    return representation


def hsv_to_hex_rgb_str(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    (R, G, B) = int(255 * r), int(255 * g), int(255 * b)
    hexval = "#" + val_to_hex_str(R) + val_to_hex_str(G) + val_to_hex_str(B)
    return hexval


class Algorithm:
    # fft_data is a time series representation of the fft
    def __init__(self, fft_data):
        self.fft_data = fft_data

    # equalizer is the most simple algorithm we might use, it simply just
    # displays the values of the fft in a circle of colors
    def equalizer(self):
        num_buckets = self.fft_data.size
        # print(final_rgb_triples)
        # print final_rgb_triples

        light_amplitude_values = np.zeros(NUM_LIGHTS)
        for i in range(num_buckets):
            # populate light_amplitude_values with the result from the fft.
            for j in range((int)(i * 1.0 * NUM_LIGHTS / num_buckets),
                           (int)((i + 1) * 1.0 * NUM_LIGHTS / num_buckets)):
                light_amplitude_values[j] = self.fft_data[i]

        final_hex_vals = np.chararray(NUM_LIGHTS, itemsize=7)
        for i in range(NUM_LIGHTS):
            final_hex_vals[i] = hsv_to_hex_rgb_str(1.0 * i / NUM_LIGHTS, 1.0,
                            light_amplitude_values[i] * 1.0 / MAX_AMPLITUDE)
        # maxd = 1
        # (r, g, b) = colorsys.hsv_to_rgb(float(depth) / maxd, 1.0, 1.0)
        # rgb = int(255 * r), int(255 * g), int(255 * b)
        # print rgb
        return final_hex_vals

    def bass_flashes(self):
        num_buckets = self.fft_data.size
        bucket_width = (MAX_BUCKET - MIN_BUCKET) * 1.0 / num_buckets
        bass_freq_diff = BASS_MAX_FREQ - MIN_BUCKET
        num_bass_buckets = (int)((bass_freq_diff) * 1.0 / bucket_width)
        all_bass_buckets = self.fft_data[0:num_bass_buckets]
        max_bass_val = np.amax(all_bass_buckets)
        all_non_bass_buckets = self.fft_data[num_bass_buckets:]
        max_non_bass_index = np.argmax(all_non_bass_buckets)
        hue_value = max_non_bass_index * 1.0 / (num_buckets - num_bass_buckets)
        val_value = max_bass_val * 1.0 / MAX_AMPLITUDE
        hex_representation = hsv_to_hex_rgb_str(hue_value, 1.0, val_value)
        final_hex_vals = np.chararray(NUM_LIGHTS, itemsize=7)
        for i in range(NUM_LIGHTS):
            final_hex_vals[i] = hex_representation
        return final_hex_vals

    def strobe(self):
        pass


data = np.array([0, 0.7, 0.4, 0.1, 0.3, 0.2, 0.1, 0.1, 0.1])
algo = Algorithm(data)
print algo.bass_flashes()
# print algo.equalizer()
