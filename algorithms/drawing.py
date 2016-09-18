#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct
import sys
import numpy as np
from PyQt4 import QtGui, QtCore


"""
ZetCode PyQt4 tutorial

In this example, we draw text in Russian azbuka.

author: Jan Bodnar
website: zetcode.com
last edited: September 2011
"""
HEIGHT = 50
LENGTH = 100
NUM_LIGHTS = LENGTH * 2 + HEIGHT * 2
STRIDE_LENGTH = 8
SIZE = 5


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

        self.locations = []

        for i in range(LENGTH):
            self.locations.append((0, LENGTH - i - 1))
        for i in range(HEIGHT):
            self.locations.append((i + 1, 0))
        for i in range(LENGTH):
            self.locations.append((HEIGHT + 1, i))
        for i in range(HEIGHT):
            self.locations.append((HEIGHT - i, LENGTH - 1))

        self.qp = QtGui.QPainter()

        self.iter = 0

    def initUI(self):
        self.text = "blah"
        width = LENGTH * STRIDE_LENGTH + 20
        height = HEIGHT * STRIDE_LENGTH + 50
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle('Draw text')
        self.show()

    def paintEvent(self, event):
        colors = get_colors(self.iter)
        self.qp.begin(self)
        self.drawRects(colors)
        self.qp.end()

    def drawRects(self, colors):
        for i in range(len(self.locations)):
            rgbtuple = struct.unpack('BBB', colors[i][1:].decode('hex'))
            (r, g, b) = rgbtuple
            self.qp.setBrush(QtGui.QColor(r, g, b))
            self.qp.drawRect(self.locations[i][1] * STRIDE_LENGTH + 10,
                        self.locations[i][0] * STRIDE_LENGTH + 10, 5, 5)

    def update(self):
        self.iter += 1
        QtGui.QWidget.update(self)
        QtCore.QTimer.singleShot(100, self.update)  # QUICKLY repeat


def get_colors(j):
    colors = np.chararray(LENGTH * 2 + HEIGHT * 2, itemsize=7)
    for i in range(NUM_LIGHTS):
        if ((i + j) % 2 == 0):
            colors[i] = "#FF00FF"
        if ((i + j) % 2 == 1):
            colors[i] = "#00FF00"
    return colors


def main():
    app = QtGui.QApplication(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Example()
    form.show()
    form.update()  # start with something
    app.exec_()
    print("DONE")
