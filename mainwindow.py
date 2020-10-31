"""GUI"""

import sys
from datetime import timedelta

from timerdialog import TimerDialog
from subclassQLabel import StretchedLabel

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

IMAGE_PLAY = 'images/play.png'
IMAGE_PAUSE = 'images/pause.png'
IMAGE_PLUS = 'images/plus.png'
IMAGE_MINUS = 'images/minus.png'

STYLESHEET_LIGHT = 'stylesheets/light.qss'
STYLESHEET_DARK = 'stylesheets/dark.qss'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("PerformanceMe")
        self.setMinimumSize(QSize(500, 600))
        

        self.tabWidget = TabWidget(self)
        self.setCentralWidget(self.tabWidget)
        
        self.show()

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

class DashboardWidget(QWidget):
    def __init__(self, parent):
        super(DashboardWidget, self).__init__(parent)
        # Define a layout to use
        self.layout = QGridLayout(self)

        # Create widgets
        self.button1 = QPushButton("But1", self)
        self.button2 = QPushButton("But2", self)

        # Add widgets
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)

class TimerWidget(QWidget):
    # pylint: disable=too-many-instance-attributes

    # Variables
    count = 60 * 45 # 45 minutes
    start = False
    tallyCalls = 0
    tallyConnects = 0
    tallyBAP = 0
    tallyMAP = 0
    tallyLAP = 0

    def __init__(self, parent):
        super(TimerWidget, self).__init__(parent)
        # Define a layout to use
        self.layout = QGridLayout(self)

        # Create widgets
        self.timerInputDialog = None
        self.setTimerButton = QPushButton("Set timer", self)
        self.timeLabel = QLabel("0:45:00", self)
        self.startStopButton = QToolButton(self)

        self.kpi = StretchedLabel("KPI", self)
        self.tally = StretchedLabel("Tally", self)

        self.calls = StretchedLabel("Calls", self)
        self.callsTally = StretchedLabel("0", self)
        self.callsTallyBtn1 = QToolButton(self)
        self.callsTallyBtn2 = QToolButton(self)

        self.connects = StretchedLabel("Connects", self)
        self.connectsTally = StretchedLabel("0", self)
        self.connectsTallyBtn1 = QToolButton(self)
        self.connectsTallyBtn2 = QToolButton(self)
        
        self.appointments = StretchedLabel("Appointments", self)

        self.bap = StretchedLabel("BAP", self)
        self.bapTally = StretchedLabel("0", self)
        self.bapTallyBtn1 = QToolButton(self)
        self.bapTallyBtn2 = QToolButton(self)

        self.map = StretchedLabel("MAP", self)
        self.mapTally = StretchedLabel("0", self)
        self.mapTallyBtn1 = QToolButton(self)
        self.mapTallyBtn2 = QToolButton(self)

        self.lap = StretchedLabel("LAP", self)
        self.lapTally = StretchedLabel("0", self)
        self.lapTallyBtn1 = QToolButton(self)
        self.lapTallyBtn2 = QToolButton(self)

        # Widget configuration
        self.setTimerButton.clicked.connect(self.SetTimerDialog)
        self.setTimerButton.setStyleSheet("font-size: 14px;")
        
        # self.timeLabelfont = QFont()
        # self.timeLabelfont.setFamily("RomanD")
        # self.timeLabelfont.setPointSize(50)
        # self.timeLabel.setFont(self.timeLabelfont)
        self.timeLabel.setStyleSheet("font-size: 50px;")

        self.startStopButton.setIcon(QIcon(IMAGE_PLAY))
        self.startStopButton.setIconSize(QSize(75, 75))
        self.startStopButton.clicked.connect(self.PlayPause)

        self.kpi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tally.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.callsTallyBtn1.setIcon(QIcon(IMAGE_MINUS))
        self.callsTallyBtn1.setIconSize(QSize(75, 75))
        self.callsTallyBtn2.setIcon(QIcon(IMAGE_PLUS))
        self.callsTallyBtn2.setIconSize(QSize(75, 75))

        self.connects.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.connectsTallyBtn1.setIcon(QIcon(IMAGE_MINUS))
        self.connectsTallyBtn1.setIconSize(QSize(75, 75))
        self.connectsTallyBtn2.setIcon(QIcon(IMAGE_PLUS))
        self.connectsTallyBtn2.setIconSize(QSize(75, 75))
        
        self.appointments.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.bapTallyBtn1.setIcon(QIcon(IMAGE_MINUS))
        self.bapTallyBtn1.setIconSize(QSize(75, 75))
        self.bapTallyBtn2.setIcon(QIcon(IMAGE_PLUS))
        self.bapTallyBtn2.setIconSize(QSize(75, 75))

        self.mapTallyBtn1.setIcon(QIcon(IMAGE_MINUS))
        self.mapTallyBtn1.setIconSize(QSize(75, 75))
        self.mapTallyBtn2.setIcon(QIcon(IMAGE_PLUS))
        self.mapTallyBtn2.setIconSize(QSize(75, 75))

        self.lapTallyBtn1.setIcon(QIcon(IMAGE_MINUS))
        self.lapTallyBtn1.setIconSize(QSize(75, 75))
        self.lapTallyBtn2.setIcon(QIcon(IMAGE_PLUS))
        self.lapTallyBtn2.setIconSize(QSize(75, 75))

        
        # Add widgets
        self.layout.addWidget(self.setTimerButton, 0, 0, 1, 4)
        self.layout.addWidget(self.timeLabel, 1, 0, 1, 3)
        self.layout.addWidget(self.startStopButton, 1, 3)

        self.layout.addWidget(self.kpi, 3, 0)
        self.layout.addWidget(self.tally, 3, 1)

        self.layout.addWidget(self.calls, 4, 0)
        self.layout.addWidget(self.callsTally, 4, 1)
        self.layout.addWidget(self.callsTallyBtn1, 4, 2)
        self.layout.addWidget(self.callsTallyBtn2, 4, 3)

        self.layout.addWidget(self.connects, 5, 0)
        self.layout.addWidget(self.connectsTally, 5, 1)
        self.layout.addWidget(self.connectsTallyBtn1, 5, 2)
        self.layout.addWidget(self.connectsTallyBtn2, 5, 3)

        # Add a separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sep.setLineWidth(1)
        self.layout.addWidget(sep, 6, 0, 1, 4)

        self.layout.addWidget(self.appointments, 7, 0, 1, 2)

        self.layout.addWidget(self.bap, 8, 0)
        self.layout.addWidget(self.bapTally, 8, 1)
        self.layout.addWidget(self.bapTallyBtn1, 8, 2)
        self.layout.addWidget(self.bapTallyBtn2, 8, 3)

        self.layout.addWidget(self.map, 9, 0)
        self.layout.addWidget(self.mapTally, 9, 1)
        self.layout.addWidget(self.mapTallyBtn1, 9, 2)
        self.layout.addWidget(self.mapTallyBtn2, 9, 3)

        self.layout.addWidget(self.lap, 10, 0)
        self.layout.addWidget(self.lapTally, 10, 1)
        self.layout.addWidget(self.lapTallyBtn1, 10, 2)
        self.layout.addWidget(self.lapTallyBtn2, 10, 3)

        # Create timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateTime)
        self.timer.start(1000)
    
    def PlayPause(self):
        if self.count != 0:
            if self.start:
                self.start = False
                self.startStopButton.setIcon(QIcon(IMAGE_PLAY))
            else:
                self.start = True
                self.startStopButton.setIcon(QIcon(IMAGE_PAUSE))

    def UpdateTime(self):
        if self.start:
            self.count -= 1
            
            if self.count == 0:
                self.timeLabel.setText("Time's up!")
                self.start = False
                self.startStopButton.setIcon(QIcon(IMAGE_PLAY))
            else:
                self.timeLabel.setText(str(timedelta(seconds=self.count)))

    def SetTimerDialog(self):
        self.timerInputDialog = TimerDialog(self)
        self.timerInputDialog.setWindowModality(Qt.ApplicationModal)
        
        if self.timerInputDialog.ok and self.timerInputDialog.number:
            print(self.timerInputDialog.number)
            self.count = self.timerInputDialog.number
            self.timeLabel.setText(str(timedelta(seconds=self.count)))
        
class SettingsWidget(QWidget):
    def __init__(self, parent):
        super(SettingsWidget, self).__init__(parent)
        self.layout = QGridLayout(self)
        # self.SetDarkStyleSheet()

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

        with open(STYLESHEET_LIGHT, 'r') as sh:
            sApp.setStyleSheet(sh.read())


    def SetDarkStyleSheet(self):
        sApp = QApplication.instance()
        if sApp is None:
            raise RuntimeError("No Application Found")

        with open(STYLESHEET_DARK, 'r') as sh:
            sApp.setStyleSheet(sh.read())

if __name__ == "__main__":
    # Create the app
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    with open(STYLESHEET_DARK, 'r') as sh:
        app.setStyleSheet(sh.read())

    window = MainWindow()
    # window.show()

    sys.exit(app.exec())
