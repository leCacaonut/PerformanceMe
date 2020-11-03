"""GUI"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QSettings, QMargins, QStandardPaths, QPoint

from constants import Name, Stylesheets, settings_fileName

from dashboardtab import DashboardWidget
from timertab import TimerWidget
from settingstab import SettingsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PerformanceMe")
        self.setMinimumSize(QSize(400, 700))
        self.resize(400, 700)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        
        self.tabWidget = TabWidget(self)
        self.setCentralWidget(self.tabWidget)

        # Setup mouse event handling
        self.oldPos = self.pos()

        self.show()

        self.initSettings()

    def initSettings(self):
        self.settings = QSettings((QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) + settings_fileName, QSettings.IniFormat)
        
        for setting in [lambda x=self.settings.value('window_position'): self.move(x),
                        self.initTheme]:
            try:
                setting()
            except Exception as e:
                print(e)


    def initTheme(self):
        sApp = QApplication.instance()
        if self.settings.value('dark_theme', type=bool) is False:
            with open(Stylesheets.light_theme, 'r') as sh:
                sApp.setStyleSheet(sh.read())
        else:
            with open(Stylesheets.dark_theme, 'r') as sh:
                sApp.setStyleSheet(sh.read())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def saveSettings(self):
        self.settings.setValue('window_position', self.pos())

    def closeEvent(self, _):
        self.saveSettings()
        for children in self.findChildren(QWidget):
            children.close()
        print("Quitting...")
        


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # Define a layout to use
        self.layout = QVBoxLayout(self)
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.documentMode()

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
        self.dashboard.setLayout(self.dashWidget.layoutBase)
        
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
    app.setOrganizationName(Name.organisation)
    app.setApplicationName(Name.program)

    window = MainWindow()
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.show()

    sys.exit(app.exec())
