import numpy as np
import pyqtgraph as pg
import pyaudio
from PyQt4 import QtCore, QtGui


class SpectrogramWidget(pg.PlotWidget):

    def __init__(self, spectrum_analyzer):
        super(SpectrogramWidget, self).__init__()

        # Make image
        self.img = pg.ImageItem()
        self.addItem(self.img)

        # Get chunk size and sample rate from spectrum analyzer
        nsamples = spectrum_analyzer.nsamples
        sample_rate = spectrum_analyzer.sample_rate

        # Instantiate image array
        self.img_array = np.zeros((1000, int(nsamples/2)+1))

        # bipolar colormap
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)

        # set colormap
        self.img.setLookupTable(lut)
        self.img.setLevels([-50,40])

        # setup the correct scaling for y-axis
        freqs = spectrum_analyzer.get_freqs()
        yscale = 1.0/(self.img_array.shape[1]/freqs[-1])
        self.img.scale((1./sample_rate)*nsamples, yscale)

        self.setLabel('left', 'Frequency', units='Hz')

        self.show()

    def update(self):

        spectrum = self.get_spectrum()

        p10 = np.percentile(spectrum, 10)
        p90 = np.percentile(spectrum, 90)

        print('p10:', p10, '\tp90:', p90)

        # roll down one and replace leading edge with new data
        self.img_array = np.roll(self.img_array, -1, 0)
        self.img_array[-1:] = spectrum

        self.img.setImage(self.img_array, autoLevels=False)

        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat
