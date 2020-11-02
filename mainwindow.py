"""GUI"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

import constants
from constants import PushButtons, Tally

from timerdialog import TimerDialog
from dashboardtab import DashboardWidget
from timertab import TimerWidget
from settingstab import SettingsWidget

class MainWindow(QMainWindow):
    test = "test"
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("PerformanceMe")
        self.setMinimumSize(QSize(400, 700))
        

        self.tabWidget = TabWidget(self)
        self.setCentralWidget(self.tabWidget)
        
        self.show()

        self.initSettings()

    def initSettings(self):
        # self.settings = QSettings()
        self.settings = QSettings(str(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)), QSettings.IniFormat)

        
        try:
            self.move(self.settings.value('window_position'))
            with open(constants.stylesheet_dark, 'r') as sh:
                app.setStyleSheet(sh.read())
        except:
            print("new settings applied")


    def closeEvent(self, _):
        self.settings.setValue('window_position', self.pos())


class TabWidget(QWidget):
    def __init__(self, parent):
        super(TabWidget, self).__init__(parent)

        # Define a layout to use
        self.layout = QVBoxLayout(self)

        # Create tab widget
        self.tabs = QTabWidget()
        # Create tabs
        self.dashboard = QWidget()
        self.timer = QWidget()
        self.settings = QWidget()

        # Setup tabs
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.timer, "Timer")
        self.tabs.addTab(self.settings, "Settings")

        # Create GUI in tabs
        self.dashWidget = DashboardWidget(self)
        self.dashboard.setLayout(self.dashWidget.layout)
        
        self.timerWidget = TimerWidget(self)
        self.timer.setLayout(self.timerWidget.layout)

        self.settingsWidget = SettingsWidget(self)
        self.settings.setLayout(self.settingsWidget.layout)

        # Add tabs
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Setup signals
        self.timerWidget.timerExpired.connect(self.dashWidget.UpdateTally)


if __name__ == "__main__":
    # Create the app
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    app.setOrganizationName(constants.name_organisation)
    app.setApplicationName(constants.name_program)

    window = MainWindow()
    # window.show()

    sys.exit(app.exec())
