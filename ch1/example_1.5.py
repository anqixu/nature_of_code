#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, qApp
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtCore import QRect, QTimer, Qt, pyqtSlot
from structs import PVector


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initUI()

        self.setup()

        self.show()

    def _initUI(self):
        self.setWindowTitle("Nature of Code")

        self.statusBar()

        menubar = self.menuBar()
        actionMenu = menubar.addMenu("&Action")

        animateAct = QAction("&Animate", self)
        animateAct.setCheckable(True)
        animateAct.setChecked(True)
        animateAct.setShortcut("A")
        animateAct.triggered.connect(self._handleAnimate)
        actionMenu.addAction(animateAct)

        stepAct = QAction("&Step", self)
        stepAct.setShortcut("S")
        stepAct.triggered.connect(self._handleStep)
        actionMenu.addAction(stepAct)

        exitAct = QAction("&Quit", self)
        exitAct.setShortcut("Q")
        exitAct.triggered.connect(qApp.quit)
        actionMenu.addAction(exitAct)

        self.timer = QTimer(self)
        self.timer.setInterval(10)  # 10ms = 100Hz
        self.timer.timeout.connect(self.update)

        self.timer.start()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def mouseMoveEvent(self, event):
        self.mousePos = PVector(event.x(), event.y())

    @pyqtSlot()
    def _handleAnimate(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    @pyqtSlot()
    def _handleStep(self):
        if not self.timer.isActive():
            self.update()

    def setup(self):
        self.mousePos = None
        self.setGeometry(100, 100, 640, 360)
        self.setMouseTracking(True)

    def draw(self, qp):
        qp.fillRect(QRect(0, 0, self.width(), self.height()), QColor(255, 255, 255))

        if self.mousePos is not None:
            mouse = PVector(self.mousePos.x, self.mousePos.y)
            center = PVector(self.width() // 2, self.height() // 2)
            mouse -= center

            m = mouse.mag()
            qp.fillRect(QRect(0, 0, m, 10), QBrush(QColor(0, 0, 0)))

            qp.setPen(QPen(QColor(0, 0, 0)))
            qp.drawLine(center.x, center.y, center.x + mouse.x, center.y + mouse.y)

    @staticmethod
    def main():
        app = QApplication(sys.argv)
        window = MyWindow()  # noqa: F841
        sys.exit(app.exec_())


if __name__ == "__main__":
    MyWindow.main()
