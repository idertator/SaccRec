import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings

from .new_test import MagicWizard
from .Signals import SignalsWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

        self.settings = QSettings('Vinculacion','EyeTracker')

        self._newTest = MagicWizard(self.settings)
        self._signalsWindow = SignalsWindow(self)

    def newMenu(self, nombre):
        menubar = self.menuBar()
        menu = menubar.addMenu(nombre)
        return menu

    def initUI(self):
        exitAct = QAction(QIcon('saccrec/gui/images/exit.svg'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        signalsAct = QAction('Signals',self)
        signalsAct.triggered.connect(self.openSignalsWindow)

        subjectAct = QAction('New Test', self)
        subjectAct.triggered.connect(self.openNewTest)

        aboutUs = QAction(QIcon('saccrec/gui/images/interrogacion.png'), '&About Us', self)

        self.statusBar()

        fileMenu = self.newMenu('&File')
        fileMenu.addAction(subjectAct)
        # fileMenu.addAction(signalsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        helpMenu = self.newMenu('&Help')
        helpMenu.addAction(aboutUs)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('EyeTracker OpenBCI')
        self.show()

    def openNewTest(self):
        self._newTest.open()

    def openSignalsWindow(self):
        self._signalsWindow.show()
