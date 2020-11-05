"""GUI"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QShortcut
from PyQt5.QtCore import Qt, QSize, QSettings, QMargins, QStandardPaths, QPoint, pyqtSlot
from PyQt5.QtGui import QIcon

from constants import Name, Stylesheets, ActionType, settings_fileName, TimerPushButtons

from dashboardtab import DashboardWidget
from timertab import TimerWidget
from detailstab import DetailsWidget
from settingstab import SettingsWidget

class MainWindow(QMainWindow):
    appraisalData = {}
    listingData = {}
    saleData = {}
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PerformanceMe")
        self.setMinimumSize(QSize(400, 700))
        self.resize(700, 700)
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        
        self.tabWidget = TabWidget(self)
        self.setCentralWidget(self.tabWidget)

        # Setup mouse event handling
        self.oldPos = self.pos()

        self.initSettings()
        self.initShortcuts()
        self.SetCurrentTabShortcuts(0)

    def initSettings(self):
        #pylint: disable=broad-except
        self.settings = QSettings((QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) + settings_fileName, QSettings.IniFormat)
        
        for setting in [lambda x=self.settings.value('window_position'): self.move(x),
                        lambda x=self.settings.value('window_size'): self.resize(x),
                        self.initTheme]:
            try:
                setting()
            except Exception as e:
                print(e)
                
        self.tabWidget.settingsWidget.stayOnTopSignal.connect(self.ToggleWindowStayOnTop)

    @pyqtSlot(bool)
    def ToggleWindowStayOnTop(self, isOnTop):
        if isOnTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def initShortcuts(self):
        # Global tab switching
        self.tabSwitchList = []
        for i in range(4):
            self.tabSwitchList.append(QShortcut("ctrl+" + str(i + 1), self))
            self.tabSwitchList[i].activated.connect(lambda x=i: self.tabWidget.tabs.setCurrentIndex(x))

        # Enable/disable shortcuts on tab change    
        self.tabWidget.tabs.currentChanged.connect(self.SetCurrentTabShortcuts)

        # Tab specific shortcuts
        self.shortcutList = []
        keyList = [
            # Dashboard
            "a", "l", "s", "g",
            # Timer
            "s", " ", "1", "2", "3", "4", "5", "shift+1", "shift+2", "shift+3", "shift+4", "shift+5"
            # Details None
            # Settings None
        ]
        
        commandList = [
            # Dashboard
            lambda: self.tabWidget.dashboardWidget.AddAction(ActionType.appraisal),
            lambda: self.tabWidget.dashboardWidget.AddAction(ActionType.listing),
            lambda: self.tabWidget.dashboardWidget.AddAction(ActionType.sale),
            self.tabWidget.dashboardWidget.SetGoals,
            # Timer
            self.tabWidget.timerWidget.SetTimerDialog,
            self.tabWidget.timerWidget.PlayPause,
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.calls_plus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.connects_plus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.BAP_plus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.MAP_plus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.LAP_plus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.calls_minus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.connects_minus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.BAP_minus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.MAP_minus),
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.LAP_minus)

            # Details None
            # Settings None
        ]

        for i, shortcuts in enumerate(keyList):
            self.shortcutList.append(QShortcut(shortcuts, self))
            self.shortcutList[i].activated.connect(commandList[i])

    def SetCurrentTabShortcuts(self, tabIndex):
        if self.tabWidget.tabs.tabText(tabIndex) == "Dashboard":
            for shortcut in self.shortcutList[:4]:
                shortcut.setEnabled(True)
            for shortcut in self.shortcutList[4:]:
                shortcut.setEnabled(False)
        elif self.tabWidget.tabs.tabText(tabIndex) == "Timer":
            for shortcut in self.shortcutList[:4]:
                shortcut.setEnabled(False)
            for shortcut in self.shortcutList[4:]:
                shortcut.setEnabled(True)
        elif self.tabWidget.tabs.tabText(tabIndex) == "Details":
            # Conveniently put this here
            self.tabWidget.detailsWidget.UpdateList()

        # elif self.tabWidget.tabs.tabText(tabIndex) == "Settings":

        # Templates
        # if self.tabWidget.tabs.tabText(tabIndex) == "Dashboard":
        # if self.tabWidget.tabs.tabText(tabIndex) == "Timer":
        # if self.tabWidget.tabs.tabText(tabIndex) == "Details":
        # if self.tabWidget.tabs.tabText(tabIndex) == "Settings":

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
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.oldPos = event.globalPos()

    def saveSettings(self):
        self.settings.setValue('window_position', self.pos())
        self.settings.setValue('window_size', self.size())

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
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setStyleSheet("font: 16px")

        # Create tabs
        self.dashboard = QWidget()
        self.timer = QWidget()
        self.details = QWidget()
        self.settings = QWidget()

        # Setup tabs
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.timer, "Timer")
        self.tabs.addTab(self.details, "Details")
        self.tabs.addTab(self.settings, "Settings")

        # Create GUI in tabs
        self.dashboardWidget = DashboardWidget(self)
        self.dashboard.setLayout(self.dashboardWidget.layoutBase)
        
        self.timerWidget = TimerWidget(self)
        self.timer.setLayout(self.timerWidget.layout)

        self.detailsWidget = DetailsWidget(self)
        self.details.setLayout(self.detailsWidget.layout)

        self.settingsWidget = SettingsWidget(self)
        self.settings.setLayout(self.settingsWidget.layout)

        # Add tabs
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Setup signals
        self.timerWidget.timerExpired.connect(self.dashboardWidget.UpdateTally)


    
if __name__ == "__main__":
    # Create the app
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    app.setOrganizationName(Name.organisation)
    app.setApplicationName(Name.program)

    window = MainWindow()
    # window.setWindowFlag(Qt.FramelessWindowHint)
    window.setWindowFlags(Qt.CustomizeWindowHint)
    
    window.setWindowIcon(QIcon('images/plus.png'))
    window.show()

    sys.exit(app.exec())
