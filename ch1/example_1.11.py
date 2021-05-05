#!/usr/bin/env python

import random
import sys

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, qApp
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import QRect, QTimer, Qt, pyqtSlot
from structs import PVector


class Mover:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.location = PVector(random.randrange(self.width), random.randrange(self.height))
        self.velocity = PVector(0, 0)
        self.topspeed = 4

    def update(self, mousePos):
        mouse = PVector(mousePos.x, mousePos.y)
        dir = mouse - self.location
        dir.normalize()
        dir *= 0.5
        acceleration = dir

        self.velocity += acceleration
        self.velocity.limit(self.topspeed)
        self.location += self.velocity

    def display(self, qp):
        qp.setPen(Qt.NoPen)
        qp.setBrush(QBrush(QColor(175, 175, 175)))
        qp.drawEllipse(int(self.location.x), int(self.location.y), 32, 32)

    def checkEdges(self):
        if self.location.x > self.width:
            self.location.x = 0
        elif self.location.x < 0:
            self.location.x = self.width

        if self.location.y > self.height:
            self.location.y = 0
        elif self.location.y < 0:
            self.location.y = self.height


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

        resetAct = QAction("&Reset", self)
        resetAct.setShortcut("R")
        resetAct.triggered.connect(self.setup)
        actionMenu.addAction(resetAct)

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
        self.setMouseTracking(True)

        self.setGeometry(100, 100, 640, 360)
        self.movers = [Mover(self.width(), self.height()) for _ in range(20)]

    def draw(self, qp):
        qp.fillRect(QRect(0, 0, self.width(), self.height()), QColor(255, 255, 255))
        if self.mousePos is not None:
            for mover in self.movers:
                mover.update(self.mousePos)
                mover.checkEdges()
                mover.display(qp)

    @staticmethod
    def main():
        app = QApplication(sys.argv)
        window = MyWindow()  # noqa: F841
        sys.exit(app.exec_())


if __name__ == "__main__":
    MyWindow.main()
