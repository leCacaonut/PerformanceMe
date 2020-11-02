"""Settings tab"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication

import constants

class SettingsWidget(QWidget):
    def __init__(self, parent):
        super(SettingsWidget, self).__init__(parent)
        self.layout = QGridLayout(self)

        # Create widgets
        self.button1 = QPushButton("Light", self)
        self.button2 = QPushButton("Dark", self)

        self.button1.clicked.connect(self.SetLightStyleSheet)
        self.button2.clicked.connect(self.SetDarkStyleSheet)

        # Add widgets
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)

    def SetLightStyleSheet(self):
        sApp = QApplication.instance()
        if sApp is None:
            raise RuntimeError("No Application Found")

        with open(constants.stylesheet_light, 'r') as sh:
            sApp.setStyleSheet(sh.read())


    def SetDarkStyleSheet(self):
        sApp = QApplication.instance()
        if sApp is None:
            raise RuntimeError("No Application Found")

        with open(constants.stylesheet_dark, 'r') as sh:
            sApp.setStyleSheet(sh.read())