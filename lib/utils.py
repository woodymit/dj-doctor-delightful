import colorsys

import numpy as np
import pyqtgraph as pg


def get_pyqt_cmap(numpy_cmap):
    rgb = np.round(np.array(numpy_cmap.colors) * 256).astype(dtype=np.ubyte)
    stops = np.linspace(0, 1, len(rgb))
    return pg.ColorMap(stops, rgb)

class CircularBuffer(object):
    def __init__(self, n, dtype=float):
        self.n = n
        self.i = 0
        self.tape = np.zeros(self.n, dtype=dtype)

    def write(self, data):
        self.tape[self.i] = data
        self.update_i()

    def update_i(self):
        self.i = self.next_i()

    def next_i(self):
        return 0 if self.i == self.n - 1 else self.i + 1

    def prev_i(self):
        return self.n - 1 if self.i == 0 else self.i - 1

    def oldest(self):
        return self.tape[self.next_i()]

    def newest(self):
        return self.tape[self.prev_i()]


# rgb_val is between 0 and 255
def val_to_hex_str(rgb_val):

    representation = str(hex(rgb_val))[2:]
    if (len(representation) == 1):
        representation = "0" + representation
    return representation


def hsv_to_hex(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    (R, G, B) = int(255 * r), int(255 * g), int(255 * b)
    hexval = "#" + val_to_hex_str(R) + val_to_hex_str(G) + val_to_hex_str(B)
    return hexval


def rgb_to_hex(rgb):
    return '#' + ''.join(map(val_to_hex_str, rgb))


def hex_to_rgb(hex_str):
    if len(hex_str) == 7:
        hex_str = hex_str[1:]
    r_str, g_str, b_str = hex_str[0:2], hex_str[2:4], hex_str[4:6]
    return (int(r_str, 16), int(g_str, 16), int(b_str, 16))


def convex_poly_ramp(x, d=2):
    return -(x - 1) ** 2 + 1
