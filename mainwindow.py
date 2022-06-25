"""The main window for the GUI"""

import os
import sys
import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QShortcut
from PyQt5.QtCore import Qt, QSize, QSettings, QMargins, QStandardPaths, QPoint, pyqtSlot
from PyQt5.QtGui import QIcon

from constants import Name, Stylesheets, ActionType, settings_file_name, data_file_name, data_file_extension, TimerPushButtons

from dashboardtab import DashboardWidget
from timertab import TimerWidget
from detailstab import DetailsWidget
from settingstab import SettingsWidget

class MainWindow(QMainWindow):
    propertyData = {}
    # appraisalData = {}
    # listingData = {}
    # saleData = {}

    appraisals = 0
    listings = 0
    sales = 0
    income = 0

    appraisalGoal = 2
    listingGoal = 1
    saleGoal = 1
    incomeGoal = 50000

    callSessions = 0
    calls = 0
    connects = 0
    appointments = 0
    buyerApts = 0
    marketApts = 0
    listingApts = 0
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PerformanceMe")
        self.setMinimumSize(QSize(400, 600))
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        
        self.tabWidget = TabWidget(self)
        self.setCentralWidget(self.tabWidget)

        # Setup mouse event handling
        self.oldPos = self.pos()

        self.initSettings()
        self.initShortcuts()
        
        # Create the save files first
        self.LoadData()
        self.SetCurrentTabShortcuts(0)

        # Get dashboard to update after loading data
        self.tabWidget.dashboardWidget.UpdateText()

    def initSettings(self): 
        #pylint: disable=broad-except
        self.settings = QSettings((QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) + settings_file_name, QSettings.IniFormat)
        
        # Using anonymous functions to run commands. Why? IDK
        for setting in [lambda x=self.settings.value('window_position', QPoint(0, 0)): self.move(x),
                        lambda x=self.settings.value('window_size', QSize(600, 600)): self.resize(x),
                        self.initTheme]:
            setting()
        
        # Connect signal
        self.tabWidget.settingsWidget.stayOnTopSignal.connect(self.ToggleWindowStayOnTop)

    def initShortcuts(self):
        # Global keys
        # Tab switching
        self.tabSwitchList = []
        for i in range(4):
            self.tabSwitchList.append(QShortcut(f"ctrl+{i + 1}", self))
            self.tabSwitchList[i].activated.connect(lambda x=i: self.tabWidget.tabs.setCurrentIndex(x))
        # Hotkeys
        # self.hotkeyList = []
        # self.hotkeyList.append(QShortcut(f"ctrl+s", self))
        # self.hotkeyList[0].activated.connect(self.SaveData)
        QShortcut(f"ctrl+s", self).activated.connect(self.SaveData)

        # Enable/disable shortcuts on tab change    
        self.tabWidget.tabs.currentChanged.connect(self.SetCurrentTabShortcuts)

        # Tab specific shortcuts
        self.shortcutList = []
        keyList = [
            # Dashboard
            "a", "l", "s", "g",
            # Timer
            "s", " ", "1", "2", "3", "4", "5", "shift+1", "shift+2", "shift+3", "shift+4", "shift+5",
            # Details
            ",", ".",
            # Settings
            "l", "d", "ctrl+n", "ctrl+o"
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
            lambda: self.tabWidget.timerWidget.PushButton(TimerPushButtons.LAP_minus),
            # Details None
            self.tabWidget.detailsWidget.ChangeSortType,
            self.tabWidget.detailsWidget.ChangeSortOrder,
            # Settings
            self.tabWidget.settingsWidget.SetLightStyleSheet,
            self.tabWidget.settingsWidget.SetDarkStyleSheet,
            self.tabWidget.settingsWidget.CreateNewSession,
            self.tabWidget.settingsWidget.OpenSaveLocation
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
            # Conveniently put this here
            self.UpdateDataCount()
            self.tabWidget.dashboardWidget.UpdateText()
        elif self.tabWidget.tabs.tabText(tabIndex) == "Timer":
            for shortcut in self.shortcutList:
                shortcut.setEnabled(False)
            for shortcut in self.shortcutList[4:16]:
                shortcut.setEnabled(True)
        elif self.tabWidget.tabs.tabText(tabIndex) == "Details":
            for shortcut in self.shortcutList:
                shortcut.setEnabled(False)
            for shortcut in self.shortcutList[16:18]:
                shortcut.setEnabled(True)
            # Conveniently put this here
            self.tabWidget.detailsWidget.UpdateList()
        elif self.tabWidget.tabs.tabText(tabIndex) == "Settings":
            for shortcut in self.shortcutList[:18]:
                shortcut.setEnabled(False)
            for shortcut in self.shortcutList[18:22]:
                shortcut.setEnabled(True)
        # Save data every time tab changes    
        self.SaveData()

    def initTheme(self):
        sApp = QApplication.instance()
        if self.settings.value('dark_theme', False, type=bool) is False:
            with open(Stylesheets.light_theme, 'r') as sh:
                sApp.setStyleSheet(sh.read())
        else:
            with open(Stylesheets.dark_theme, 'r') as sh:
                sApp.setStyleSheet(sh.read())

    def LoadData(self):
        if not os.path.exists(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)):
            os.makedirs(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
        try:
            with open(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_file_name + data_file_extension, 'r') as file:
                try:
                    jsonData = json.load(file)
                    # Default values are already set at start of class

                    self.propertyData = jsonData.get('propertydata', self.propertyData)
                    # self.appraisalData = jsonData.get('appraisaldata', self.appraisalData)
                    # self.listingData = jsonData.get('listingdata', self.listingData)
                    # self.saleData = jsonData.get('saledata', self.saleData)
                    
                    self.appraisalGoal = jsonData.get('appraisalgoal', self.appraisalGoal)
                    self.listingGoal = jsonData.get('listinggoal', self.listingGoal)
                    self.saleGoal = jsonData.get('salegoal', self.saleGoal)
                    self.incomeGoal = jsonData.get('incomegoal', self.incomeGoal)
                    self.callSessions = jsonData.get('call_sessions', self.callSessions)
                    self.calls = jsonData.get('calls', self.calls)
                    self.connects = jsonData.get('connects', self.connects)
                    self.appointments = jsonData.get('appointments', self.appointments)
                    self.buyerApts = jsonData.get('buyerApts', self.buyerApts)
                    self.marketApts = jsonData.get('marketApts', self.marketApts)
                    self.listingApts = jsonData.get('listingApts', self.listingApts)
                
                except json.JSONDecodeError as e:
                    print(e)
                
        except FileNotFoundError as e:
            print("FILENOTFOUND: " + f"{e}")
            self.SaveData()

        self.UpdateDataCount()

    def SaveSettings(self):
        self.settings.setValue('window_position', self.pos())
        self.settings.setValue('window_size', self.size())

    def SaveData(self):
        # print("Saving data...")
        data = {
            'propertydata': self.propertyData,
            'appraisalgoal': self.appraisalGoal,
            'listinggoal': self.listingGoal,
            'salegoal': self.saleGoal,
            'incomegoal': self.incomeGoal,
            'call_sessions': self.callSessions,
            'calls': self.calls,
            'connects': self.connects,
            'appointments': self.appointments,
            'buyerApts': self.buyerApts,
            'marketApts': self.marketApts,
            'listingApts': self.listingApts
        }

        with open(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_file_name + data_file_extension, 'w+') as file:
            json.dump(data, file, indent=4)

    def ResetData(self):
        self.propertyData = {}
        self.appraisals = 0
        self.listings = 0
        self.sales = 0
        self.income = 0
        self.appraisalGoal = 2
        self.listingGoal = 1
        self.saleGoal = 1
        self.incomeGoal = 50000
        self.callSessions = 0
        self.calls = 0
        self.connects = 0
        self.appointments = 0
        self.buyerApts = 0
        self.marketApts = 0
        self.listingApts = 0

    @pyqtSlot(bool)
    def ToggleWindowStayOnTop(self, isOnTop):
        if isOnTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def UpdateDataCount(self):
        # Calculate number of appraisals, listings, sales, income
        # See if an action's date exists
        self.appraisals = self.listings = self.sales = self.income = 0
        for data in self.propertyData:
            if 'appraisal_date' in self.propertyData[data]:
                self.appraisals += 1
            if 'listing_date' in self.propertyData[data]:
                self.listings += 1
            if 'sale_date' in self.propertyData[data]:
                self.sales += 1
                self.income += self.propertyData[data]['price'] * self.propertyData[data]['commission'] / 100

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.oldPos = event.globalPos()

    def closeEvent(self, _):
        self.SaveSettings()
        self.SaveData()
        for children in self.findChildren(QWidget):
            children.close()
        # print("Quitting...")
        

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
        self.timerWidget.saveData.connect(self.dashboardWidget.UpdateTally)


    
if __name__ == "__main__":
    # Create the app
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    app.setOrganizationName(Name.organisation)
    app.setApplicationName(Name.program)

    window = MainWindow()
    # window.setWindowFlag(Qt.FramelessWindowHint)
    window.setWindowFlags(Qt.CustomizeWindowHint)
    
    window.setWindowIcon(QIcon('images/icon.ico'))
    window.show()

    sys.exit(app.exec())
