"""Settings tab"""

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QCheckBox
from PyQt5.QtCore import Qt, QSettings, QStandardPaths, pyqtSignal

from constants import settings_fileName, Stylesheets

class SettingsWidget(QWidget):
    stayOnTopSignal = pyqtSignal(bool)

    stayOnTop = False
    
    def __init__(self, parent):
        super().__init__(parent)
        self.settings = QSettings((QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) + settings_fileName, QSettings.IniFormat)
        try:
            self.stayOnTop = self.settings.value('stay_on_top')
        except Exception as e:
            print(e)
            self.stayOnTop = False

        try:
            self.darkTheme = self.settings.value('dark_theme')
        except Exception as e:
            print(e)
            self.darkTheme = False

        self.layout = QGridLayout(self)

        # Create widgets
        self.stayOnTopCheckBox = QCheckBox("Stay on top", self)
        self.lightThemeButton = QPushButton("Light", self)
        self.darkThemeButton = QPushButton("Dark", self)

        # Setup widgets
        self.stayOnTopCheckBox.stateChanged.connect(lambda: self.ToggleWindowStayOnTop(self.stayOnTopCheckBox))
        self.lightThemeButton.clicked.connect(self.SetLightStyleSheet)
        self.darkThemeButton.clicked.connect(self.SetDarkStyleSheet)


        # Add widgets
        self.layout.addWidget(self.stayOnTopCheckBox, 0, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.lightThemeButton, 1, 0)
        self.layout.addWidget(self.darkThemeButton, 1, 1)

    def SetLightStyleSheet(self):
        self.darkTheme = False
        sApp = QApplication.instance()
        if sApp is None:
            return
        try:
            with open(Stylesheets.light_theme, 'r') as sh:
                sApp.setStyleSheet(sh.read())
        except Exception as e:
            print(e)

    def SetDarkStyleSheet(self):
        self.darkTheme = True
        sApp = QApplication.instance()
        if sApp is None:
            return
        try:
            with open(Stylesheets.dark_theme, 'r') as sh:
                sApp.setStyleSheet(sh.read())
        except Exception as e:
            print(e)

    def ToggleWindowStayOnTop(self, isOnTop):
        self.stayOnTop = isOnTop.isChecked()
        self.stayOnTopSignal.emit(self.stayOnTop)

    def SaveSettings(self):
        self.settings.setValue('dark_theme', self.darkTheme)
        self.settings.setValue('stay_on_top', self.stayOnTop)

    def closeEvent(self, _):
        self.SaveSettings()
