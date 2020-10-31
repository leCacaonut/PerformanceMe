"""GUI"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

PLAY_IMAGE = 'images/play.png'
PAUSE_IMAGE = 'images/pause.png'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PerformanceMe")
        self.setMinimumSize(QSize(600, 800))

        # self.UI()
        self.tabWidget = TabWidget()
        self.tabWidget.setLayout(self.tabWidget.layout)
        self.setCentralWidget(self.tabWidget)
        self.show()

class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        # Define a layout to use
        self.layout = QGridLayout(self)

        # Tab screen
        self.tabs = QTabWidget()
        self.dashboard = QWidget()
        self.timer = QWidget()
        # self.tabs.resize(400, 500)

        # Setup tabs
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.timer, "Timer")

        # Create GUI in tabs
        self.dashWidget = DashboardWidget()
        self.dashboard.setLayout(self.dashWidget.layout)
        self.timerWidget = TimerWidget()
        self.timer.setLayout(self.timerWidget.layout)

        # Add tabs
        self.layout.addWidget(self.tabs)

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Define a layout to use
        self.layout = QGridLayout(self)

        # Create widgets
        self.button1 = QPushButton("But1")
        self.button2 = QPushButton("But2")

        # Add widgets
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)

class TimerWidget(QWidget):
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        # Variables
        self.count = 0
        self.start = False

        # Define a layout to use
        self.layout = QGridLayout(self)

        # Create widgets
        self.setTimeButton = QPushButton("Set time")
        self.timeLabel = QLabel("1:00:00")
        self.startStopButton = QToolButton()

        # Widget configuration
        self.setTimeButton.clicked.connect(self.SetTimer)
        self.setTimeButton.setStyleSheet("color:rgb(59, 64, 84)")
        
        self.timeLabelfont = QFont()
        self.timeLabelfont.setFamily("RomanD")
        self.timeLabelfont.setPointSize(50)
        self.timeLabel.setFont(self.timeLabelfont)
        self.timeLabel.setStyleSheet("color:rgb(59, 64, 84)")

        self.startStopButton.setIcon(QIcon(PLAY_IMAGE))
        self.startStopButton.setIconSize(QSize(75, 75))
        self.startStopButton.clicked.connect(self.PlayPause)
        
        # Add widgets
        self.layout.addWidget(self.setTimeButton, 0, 0, 1, 2)
        self.layout.addWidget(self.timeLabel, 1, 0)
        self.layout.addWidget(self.startStopButton, 1, 1)

        # Create timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.UpdateTime)
        self.timer.start(1000)

    def SetTimer(self):
        self.count = 10
        self.timeLabel.setText(str(self.count))

    def PlayPause(self):
        if self.count != 0:
            if self.start:
                self.start = False
                self.startStopButton.setIcon(QIcon(PLAY_IMAGE))
            else:
                self.start = True
                self.startStopButton.setIcon(QIcon(PAUSE_IMAGE))
                
                
            

    def UpdateTime(self):
        if self.start:
            self.count -= 1
            
            if self.count == 0:
                self.timeLabel.setText("Time's up!")
                self.start = False
            else:
                self.timeLabel.setText(str(self.count))

            

if __name__ == "__main__":
    # Create the app
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
