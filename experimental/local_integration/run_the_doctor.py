from PyQt4 import QtGui, QtCore
import sys
import numpy as np
import pyqtgraph
import SWHear



class ToolStack(object):
    def __init__(self, sampler, vis_alg, light_controller):
        self.sampler = sampler
        self.vis_alg = vis_alg
        self.light_controller = light_controller

        # Begin sampling
        self.sampler.stream_start()
        self.keep_running = True

    def update(self):
        if self.sampler.data is not None and self.sampler.fft is not None:
            rgb = self.vis_alg.get_rgb(self.sampler.fft[:500])
            self.light_controller.send_rgb(rgb)

        if self.keep_running:
            QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat

    def close(self):
        self.keep_running = False
        self.sampler.close()


class QTApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        super(QTApp, self).__init__(parent)
        self.setupUi(self)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT = 0
        self.maxPCM = 0
        self.ear = SWHear.SWHear()
        self.ear.stream_start()

    def plot_fft(self):
        pcmMax = np.max(np.abs(self.ear.data))
        if pcmMax > self.maxPCM:
            self.maxPCM = pcmMax
            self.grPCM.plotItem.setRange(yRange=[-pcmMax, pcmMax])
        if np.max(self.ear.fft) > self.maxFFT:
            self.maxFFT = np.max(np.abs(self.ear.fft))
            self.grFFT.plotItem.setRange(yRange=[0, self.maxFFT])
        self.pbLevel.setValue(1000 * pcmMax / self.maxPCM)
        pen = pyqtgraph.mkPen(color='b')
        self.grPCM.plot(self.ear.datax, self.ear.data,
                        pen=pen, clear=True)
        pen = pyqtgraph.mkPen(color='r')
        self.grFFT.plot(self.ear.fftx[:500], self.ear.fft[:500],
                        pen=pen, clear=True)


if __name__ == "__main__":
    app = LocalApp()
    app.show()
    app.update()  # start with something
    print("DONE")
