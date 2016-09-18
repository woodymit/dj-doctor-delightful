#!/usr/bin/python
# -*- coding: utf-8 -*-
import utils

import sys
import numpy as np
from PyQt4 import QtGui, QtCore


class QTLightSim(QtGui.QWidget):
    def __init__(self, height=50, length=100, stride=8, size=5):

        self.height = height
        self.length = length
        self.stride = stride
        self.size = size

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
        self.setWindowTitle('Draw text')
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        # colors = self.get_colors(self.iter)
        hex_colors = self.get_hex_arr()
        self.drawRects(hex_colors)
        self.qp.end()

    def drawRects(self, hex_colors):
        for hex_color, loc in zip(hex_colors, self.locations):
            rgbtuple = utils.hex_to_rgb(hex_color)
            self.qp.setBrush(QtGui.QColor(*rgbtuple))
            self.qp.drawRect(loc[1] * self.stride + 10,
                    loc[0] * self.stride + 10, self.size, self.size)

    def update(self):
        if self.get_hex_arr is None:
            raise Exception('Pls assign me a get_hex_arr func')

        self.iter += 1
        QtGui.QWidget.update(self)
        QtCore.QTimer.singleShot(100, self.update)  # QUICKLY repeat


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
    lights.update()  # start with something

    app.exec_()
    print("DONE")
