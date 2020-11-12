"""Settings tab"""

from os import rename, startfile
from datetime import datetime

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QGridLayout, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt, QSettings, QStandardPaths, pyqtSignal

from constants import settings_file_name, data_file_name, data_file_extension, Stylesheets, shortcut_help

class SettingsWidget(QWidget):
    stayOnTopSignal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.settings = QSettings((QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) + settings_file_name, QSettings.IniFormat)
        try:
            self.stayOnTop = self.settings.value('stay_on_top', False)
        except Exception as e:
            print(e)

        try:
            self.darkTheme = self.settings.value('dark_theme', False)
        except Exception as e:
            print(e)

        self.layout = QGridLayout(self)

        # Create widgets
        self.shortcutLabel = QLabel(self)
        self.stayOnTopCheckBox = QCheckBox("Stay on top", self)
        self.lightThemeButton = QPushButton("Light", self)
        self.darkThemeButton = QPushButton("Dark", self)
        self.createNewSession = QPushButton("Create a new session", self)
        self.openSaveLocation = QPushButton("View saved data", self)

        # Setup widgets
        self.shortcutLabel.setText(shortcut_help)
        self.stayOnTopCheckBox.stateChanged.connect(lambda: self.ToggleWindowStayOnTop(self.stayOnTopCheckBox))
        self.shortcutLabel.setWordWrap(True)
        self.lightThemeButton.clicked.connect(self.SetLightStyleSheet)
        self.darkThemeButton.clicked.connect(self.SetDarkStyleSheet)
        self.createNewSession.clicked.connect(self.CreateNewSession)
        self.openSaveLocation.clicked.connect(self.OpenSaveLocation)

        # Add widgets
        self.layout.addWidget(self.shortcutLabel, 0, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.stayOnTopCheckBox, 1, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.lightThemeButton, 2, 0)
        self.layout.addWidget(self.darkThemeButton, 2, 1)
        self.layout.addWidget(self.createNewSession, 3, 0)
        self.layout.addWidget(self.openSaveLocation, 3, 1)

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
        self.stayOnTopSignal.emit(isOnTop.isChecked())

    def CreateNewSession(self):
        errormsg = QMessageBox(QMessageBox.Warning, "Caution", "Create new session?", QMessageBox.Ok | QMessageBox.Cancel, self)
        errormsg.setDefaultButton(QMessageBox.Cancel)
        errormsg.setWindowFlag(Qt.FramelessWindowHint)
        if errormsg.exec() == QMessageBox.Cancel:
            return

        self.parent().parent().SaveData()
        try:
            rename(
                QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_file_name + data_file_extension,
                QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_file_name + datetime.now().strftime('%Y%m%d-%H%M%S') + data_file_extension
            )
        except WindowsError as e:
            print(e)
            errormsg = QMessageBox(QMessageBox.Critical, "ERROR", "Could not create a new session! Try again later.", QMessageBox.Ok, self)
            errormsg.setWindowFlag(Qt.FramelessWindowHint)
            errormsg.show()
            return

        # Will create file if not exist
        self.parent().parent().LoadData()

    def OpenSaveLocation(self):
        startfile(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))

    def SaveSettings(self):
        self.settings.setValue('dark_theme', self.darkTheme)

    def closeEvent(self, _):
        self.SaveSettings()
