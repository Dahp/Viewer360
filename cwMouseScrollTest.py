import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QTransform
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class MyPlotWidget(pg.PlotWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__()
        self.resize(400, 200)
        self.setMouseTracking(True)

        self.graphWidget = MyPlotWidget()
        self.graphWidget.setMouseEnabled(x=False, y=False)
        data = np.random.randn(10)
        self.graphWidget.plot(data)

        myLayout = QHBoxLayout()
        myLayout.addWidget(self.graphWidget)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(myLayout)

        self.zoom = 1
        self.rotate = 0

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F11:
            self.toggleFullscreen()
        elif event.key() == QtCore.Qt.Key_Equal or event.key() == QtCore.Qt.Key_E:
            self.zoomIn()
        elif event.key() == QtCore.Qt.Key_Minus or event.key() == QtCore.Qt.Key_D:
            self.zoomOut()
        elif event.key() == QtCore.Qt.Key_1:
            self.zoomReset()

    def zoomIn(self):
        self.zoom *= 1.05
        self.updateView()

    def zoomOut(self):
        self.zoom /= 1.05
        self.updateView()

    def zoomReset(self):
        self.zoom = 1
        self.updateView()

    def updateView(self):
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))


def window():
    app = QApplication(sys.argv)
    win = MainWidget()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()