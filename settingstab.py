"""Settings tab"""

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout
from PyQt5.QtCore import QSettings, QStandardPaths

from constants import settings_fileName, Stylesheets

class SettingsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

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

        with open(Stylesheets.light_theme, 'r') as sh:
            sApp.setStyleSheet(sh.read())

        settings = QSettings((QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) + settings_fileName, QSettings.IniFormat)

        settings.setValue('dark_theme', False)


    def SetDarkStyleSheet(self):
        sApp = QApplication.instance()
        if sApp is None:
            raise RuntimeError("No Application Found")

        with open(Stylesheets.dark_theme, 'r') as sh:
            sApp.setStyleSheet(sh.read())

        settings = QSettings((QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) + settings_fileName, QSettings.IniFormat)

        settings.setValue('dark_theme', True)
        