# -*- coding: utf-8 -*-
"""
This example demonstrates the use of RemoteGraphicsView to improve performance in
applications with heavy load. It works by starting a second process to handle 
all graphics rendering, thus freeing up the main process to do its work.

In this example, the update() function is very expensive and is called frequently.
After update() generates a new set of data, it can either plot directly to a local
plot (bottom) or remotely via a RemoteGraphicsView (top), allowing speed comparison
between the two cases. IF you have a multi-core CPU, it should be obvious that the 
remote case is much faster.
"""

# import initExample ## Add path to library (just for examples; you do not
# need this)
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.widgets.RemoteGraphicsView
import numpy as np


class RemoteSamplePlotter(object):

    label_text = 'Remote Sample Plotter'
    window_dim = [800, 800]

    def __init__(self):
        self.start()

    def start(self):
        self.app = pg.mkQApp()

        # Make remote graphics view
        self.view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        # Prettier plots at no cost to the main process
        self.view.pg.setConfigOptions(antialias=True)
        self.view.setWindowTitle(self.label_text)

        # Add remote view and label to layour
        self.label = QtGui.QLabel()
        self.layout = pg.LayoutWidget()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.view, row=1, col=0, colspan=3)
        self.layout.resize(*self.window_dim)
        self.layout.show()

        # Make a PlotItem in the remote process that will be displayed locally
        self.rplt = self.view.pg.PlotItem()
        self.rplt._setProxyOptions(
                deferGetattr=True) # speeds up access to rplt.plot
        self.view.setCentralItem(self.rplt)

        self.lastUpdate = pg.ptime.time()
        self.avgFps = 0.0


    def update(self):
        # global check, label, plt, lastUpdate, avgFps, rpltfunc
        data = np.random.normal(size=(10000, 50)).sum(axis=1)
        data += 5 * np.sin(np.linspace(0, 10, data.shape[0]))

        # We do not expect a return value.
        self.rplt.plot(data, clear=True, _callSync='off')
        # By turning off callSync, we tell
        # the proxy that it does not need to
        # wait for a reply from the remote
        # process.

        now = pg.ptime.time()
        fps = 1.0 / (now - self.lastUpdate)
        self.lastUpdate = now
        self.avgFps = self.avgFps * 0.8 + fps * 0.2
        self.label.setText("Generating %0.2f fps" % self.avgFps)

        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        plotter = RemoteSamplePlotter()
        plotter.update()
        QtGui.QApplication.instance().exec_()
