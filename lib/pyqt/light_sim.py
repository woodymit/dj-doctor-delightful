#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import utils

import sys
import numpy as np
from PyQt4 import QtGui, QtCore


class CircularBuffer(object):
    def __init__(self, n, dtype):
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


class QTLightSim(QtGui.QWidget):

    fps_sample_window = 10

    def __init__(self, height=19, length=31, stride=32, size=30):

        self.height = height
        self.length = length
        self.stride = stride
        self.size = size
        self.times = CircularBuffer(self.fps_sample_window, float)
        self.fps = 0

        super(QTLightSim, self).__init__()
        self.initUI()

        self.locations = []
        for i in range(length):
            self.locations.append((0, length - i - 1))
        for i in range(height):
            self.locations.append((i + 1, 0))
        for i in range(length):
            self.locations.append((height + 1, i))
        for i in range(height):
            self.locations.append((height - i, length - 1))
        self.nlights = len(self.locations)

        self.qp = QtGui.QPainter()

        self.iter = 0
        self.get_hex_arr = None


    def initUI(self):
        self.text = "blah"
        width = self.length * self.stride + 20
        height = self.height * self.stride + 50
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle('QT Light Sim')
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        hex_colors, freq_staleness = self.get_hex_arr()
        self.drawBG()
        self.drawRects(hex_colors)
        if self.iter % 100 == 0:
            self.recordFPS()
        self.drawFPS(event)

        if freq_staleness:
            stale_msg = 'freq staleness:{0}'.format(freq_staleness)
        else:
            stale_msg = '0 freq latency'
        self.drawText(event, stale_msg, 60, 80)

        self.qp.end()

    def calcFPS(self):
        fps = (self.fps_sample_window - 1) / (
                self.times.newest() - self.times.oldest())
        assert max(self.times.tape) == self.times.newest()
        return fps

    def recordFPS(self):
        self.fps = self.calcFPS()

    def drawFPS(self, event):
        fps_msg = 'FPS:{0}'.format(self.fps)
        self.drawText(event, fps_msg)

    def drawText(self, event, text, x=None, y=None):
        self.qp.setPen(QtGui.QColor(168, 34, 3))
        self.qp.setFont(QtGui.QFont('Decorative', 16))
        if x is None and y is None:
            self.qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text)
        elif x is not None and y is not None:
            self.qp.drawText(x, y, text)
        else:
            raise ValueError('Give me both x and y or neither')

    def drawBG(self):
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        self.qp.setBrush(brush)
        self.qp.drawRect(0, 0, 2000, 2000)

    def drawRects(self, hex_colors):
        for hex_color, loc in zip(hex_colors, self.locations):
            rgbtuple = utils.hex_to_rgb(hex_color)
            self.qp.setBrush(QtGui.QColor(*rgbtuple))
            self.qp.drawRect(loc[1] * self.stride + 10,
                    loc[0] * self.stride + 10, self.size, self.size)

    def update(self):
        if self.get_hex_arr is None:
            raise Exception('Pls assign me a get_hex_arr func')

        # t = time.clock()
        t = time.time()
        self.times.write(t)

        self.iter += 1
        QtGui.QWidget.update(self)
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat


    def get_colors(self, j):
        colors = np.chararray(self.nlights, itemsize=7)
        for i in range(self.nlights):
            if ((i + j) % 2 == 0):
                colors[i] = "#FF00FF"
            if ((i + j) % 2 == 1):
                colors[i] = "#00FF00"
        return colors


def main():
    app = QtGui.QApplication()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    lights = QTLightSim()

    def get_hex_arr():
        return ['#FF0000'] * lights.nlights
    lights.get_hex_arr = get_hex_arr

    lights.show()
    lights.update()

    app.exec_()
    print("DONE")
