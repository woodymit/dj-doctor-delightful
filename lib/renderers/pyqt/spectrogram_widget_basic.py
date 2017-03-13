import time
import utils

import numpy as np
import pyqtgraph as pg
import pyaudio
from PyQt4 import QtCore, QtGui

import matplotlib.pyplot as plt

class SpectrogramWidget(pg.PlotWidget):

    read_collected = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, shape, autolevel_period=4):
        super(SpectrogramWidget, self).__init__()

        self.autolevel_period = autolevel_period

        self.crop_index = None

        # Make image
        self.img = pg.ImageItem()
        self.addItem(self.img)

        # Instantiate image array
        self.img_array = np.zeros(shape)

        # Get colormap
        np_cmap = plt.get_cmap('viridis')
        cmap = utils.get_pyqt_cmap(np_cmap)
        lut = cmap.getLookupTable(0.0, 1.0, 256, alpha=False)

        # Set colormap
        self.img.setLookupTable(lut)
        self.img.setLevels([5000,500000])

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.last_autolevel = 0

        self.show()

    def auto_set_levels(self, spectrum):
        p05 = np.percentile(spectrum, 5)
        p95 = np.percentile(spectrum, 95)
        self.img.setLevels([p05, p95])

        print('min:', spectrum.min(),'\tp05:', p05, '\tp95:', p95, '\tmax:', spectrum.max())

    def periodic_set_levels(self):
        t = time.time()
        time_since_autolevel =  t - self.last_autolevel
        if time_since_autolevel > self.autolevel_period:
            self.last_autolevel = t
            self.auto_set_levels(self.img_array)

    def update(self, chunk):

        spectrum = self.get_spectrum(chunk)[:self.crop_index]

        # Roll down one and replace leading edge with new data
        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = spectrum

        self.img.setImage(self.img_array, autoLevels=False)
        self.periodic_set_levels()


