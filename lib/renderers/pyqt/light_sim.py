#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import settings
import utils

import sys
import numpy as np
from PyQt4 import QtGui, QtCore


class QTLightSim(QtGui.QWidget):

    fps_sample_window = 10

    def __init__(self, height=19, length=31, stride=32, size=30):

        self.app = QtGui.QApplication(sys.argv)

        self.height = height
        self.length = length
        self.stride = stride
        self.size = size
        self.times = utils.CircularBuffer(self.fps_sample_window, float)
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
        hex_colors = self.get_hex_arr()
        self.drawBG()
        self.drawRects(hex_colors)

        if settings.FPS_MONITOR:
            # Update self.FPS
            if self.iter % 100 == 0:
                self.recordFPS()

            # Display FPS
            fps_msg = 'FPS:{:28.0f}'.format(self.fps)
            self.drawText(event, fps_msg, 60, 80)

        self.qp.end()

    def calcFPS(self):
        if (self.times.newest() == self.times.oldest()):
            fps = -1
        else:
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
        assert len(hex_colors) == len(self.locations)
        for hex_color, loc in zip(hex_colors, self.locations):
            rgbtuple = utils.hex_to_rgb(hex_color)
            self.qp.setBrush(QtGui.QColor(*rgbtuple))
            self.qp.drawRect(loc[1] * self.stride + 10,
                    loc[0] * self.stride + 10, self.size, self.size)

    def update(self):

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

    def start(self):
        if self.get_hex_arr is None:
            raise Exception('Pls assign me a get_hex_arr func')

        self.update()
        self.app.exec_()

    def close(self):
        self.app.quit()


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
