"""Timer tab"""

# Standard
from datetime import timedelta

# Third party
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QToolButton, QFrame, QSizePolicy, QMessageBox
from PyQt5.QtCore import pyqtSignal, QSize, QTimer, Qt
from PyQt5.QtGui import QIcon

# First party
from constants import default_icon_size, Tally, TimerPushButtons, Images

from customsubclasses import StretchedLabel
from timerpopup import TimerDialog

class TimerWidget(QWidget):
    # pylint: disable=too-many-instance-attributes
    saveData = pyqtSignal(Tally)

    # Variables
    count = 60 * 45 # 45 minutes
    start = False

    tally = Tally()

    def __init__(self, parent):
        super().__init__(parent)
        # self.saveData.connect()

        # Define a layout to use
        self.layout = QGridLayout(self)

        # Create widgets
        self.timerInputDialog = None
        self.setTimerButton = QPushButton("Set timer", self)
        self.timeLabel = QLabel(f"{timedelta(seconds=self.count)}", self)
        self.stopButton = QToolButton(self)
        self.startPauseButton = QToolButton(self)

        self.lkpi = StretchedLabel("KPI", self)
        self.ltally = StretchedLabel("Tally", self)

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
        self.setTimerButton.setStyleSheet("font-size: 16px;")
        
        self.lkpi.setStyleSheet("font-size: 26px;")
        self.ltally.setStyleSheet("font-size: 26px;")
        self.calls.setStyleSheet("font-size: 26px;")
        self.callsTally.setStyleSheet("font-size: 26px;")
        self.connects.setStyleSheet("font-size: 26px;")
        self.connectsTally.setStyleSheet("font-size: 26px;")
        self.appointments.setStyleSheet("font-size: 26px;")
        self.bap.setStyleSheet("font-size: 26px;")
        self.bapTally.setStyleSheet("font-size: 26px;")
        self.map.setStyleSheet("font-size: 26px;")
        self.mapTally.setStyleSheet("font-size: 26px;")
        self.lap.setStyleSheet("font-size: 26px;")
        self.lapTally.setStyleSheet("font-size: 26px;")
        
        self.timeLabel.setStyleSheet("font-size: 50px;")

        self.stopButton.setIcon(QIcon(Images.stop))
        self.stopButton.setIconSize(QSize(default_icon_size, default_icon_size))
        self.stopButton.clicked.connect(self.EndSession)

        self.startPauseButton.setIcon(QIcon(Images.play))
        self.startPauseButton.setIconSize(QSize(default_icon_size, default_icon_size))
        self.startPauseButton.clicked.connect(self.PlayPause)

        self.lkpi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ltally.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.callsTallyBtn1.setIcon(QIcon(Images.minus))
        self.callsTallyBtn1.setIconSize(QSize(default_icon_size, default_icon_size))
        self.callsTallyBtn1.clicked.connect(lambda state, x=TimerPushButtons.calls_minus: self.PushButton(x))
        self.callsTallyBtn2.setIcon(QIcon(Images.plus))
        self.callsTallyBtn2.setIconSize(QSize(default_icon_size, default_icon_size))
        self.callsTallyBtn2.clicked.connect(lambda state, x=TimerPushButtons.calls_plus: self.PushButton(x))

        self.connects.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.connectsTallyBtn1.setIcon(QIcon(Images.minus))
        self.connectsTallyBtn1.setIconSize(QSize(default_icon_size, default_icon_size))
        self.connectsTallyBtn1.clicked.connect(lambda state, x=TimerPushButtons.connects_minus: self.PushButton(x))
        self.connectsTallyBtn2.setIcon(QIcon(Images.plus))
        self.connectsTallyBtn2.setIconSize(QSize(default_icon_size, default_icon_size))
        self.connectsTallyBtn2.clicked.connect(lambda state, x=TimerPushButtons.connects_plus: self.PushButton(x))
        
        self.appointments.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.bapTallyBtn1.setIcon(QIcon(Images.minus))
        self.bapTallyBtn1.setIconSize(QSize(default_icon_size, default_icon_size))
        self.bapTallyBtn1.clicked.connect(lambda _, x=TimerPushButtons.BAP_minus: self.PushButton(x))
        self.bapTallyBtn2.setIcon(QIcon(Images.plus))
        self.bapTallyBtn2.setIconSize(QSize(default_icon_size, default_icon_size))
        self.bapTallyBtn2.clicked.connect(lambda _, x=TimerPushButtons.BAP_plus: self.PushButton(x))

        self.mapTallyBtn1.setIcon(QIcon(Images.minus))
        self.mapTallyBtn1.setIconSize(QSize(default_icon_size, default_icon_size))
        self.mapTallyBtn1.clicked.connect(lambda _, x=TimerPushButtons.MAP_minus: self.PushButton(x))
        self.mapTallyBtn2.setIcon(QIcon(Images.plus))
        self.mapTallyBtn2.setIconSize(QSize(default_icon_size, default_icon_size))
        self.mapTallyBtn2.clicked.connect(lambda _, x=TimerPushButtons.MAP_plus: self.PushButton(x))

        self.lapTallyBtn1.setIcon(QIcon(Images.minus))
        self.lapTallyBtn1.setIconSize(QSize(default_icon_size, default_icon_size))
        self.lapTallyBtn1.clicked.connect(lambda _, x=TimerPushButtons.LAP_minus: self.PushButton(x))
        self.lapTallyBtn2.setIcon(QIcon(Images.plus))
        self.lapTallyBtn2.setIconSize(QSize(default_icon_size, default_icon_size))
        self.lapTallyBtn2.clicked.connect(lambda _, x=TimerPushButtons.LAP_plus: self.PushButton(x))

        
        # Add widgets
        self.layout.addWidget(self.setTimerButton, 0, 0, 1, 4)
        self.layout.addWidget(self.timeLabel, 1, 0, 1, 3)
        self.layout.addWidget(self.stopButton, 1, 2)
        self.layout.addWidget(self.startPauseButton, 1, 3)

        self.layout.addWidget(self.lkpi, 3, 0)
        self.layout.addWidget(self.ltally, 3, 1)

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
        # sep.setLineWidth(1)
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

    def PushButton(self, button):
        if self.start is False:
            errormsg = QMessageBox(QMessageBox.Critical, "ERROR", "Start the timer first!", QMessageBox.Ok, self)
            errormsg.setWindowFlag(Qt.FramelessWindowHint)
            errormsg.exec()
            return

        if button == TimerPushButtons.calls_minus:
            if self.tally.calls > 0:
                self.tally.calls -= 1
            self.callsTally.setText(f"{self.tally.calls}")
        if button == TimerPushButtons.calls_plus:
            self.tally.calls += 1
            self.callsTally.setText(f"{self.tally.calls}")

        if button == TimerPushButtons.connects_minus:
            if self.tally.connects > 0:
                self.tally.connects -= 1
            self.connectsTally.setText(f"{self.tally.connects}")
        if button == TimerPushButtons.connects_plus:
            self.tally.connects += 1
            self.connectsTally.setText(f"{self.tally.connects}")
        
        if button == TimerPushButtons.BAP_minus:
            if self.tally.BAP > 0:
                self.tally.BAP -= 1
            self.bapTally.setText(f"{self.tally.BAP}")
        if button == TimerPushButtons.BAP_plus:
            self.tally.BAP += 1
            self.bapTally.setText(f"{self.tally.BAP}")

        if button == TimerPushButtons.MAP_minus:
            if self.tally.MAP > 0:
                self.tally.MAP -= 1
            self.mapTally.setText(f"{self.tally.MAP}")
        if button == TimerPushButtons.MAP_plus:
            self.tally.MAP += 1
            self.mapTally.setText(f"{self.tally.MAP}")

        if button == TimerPushButtons.LAP_minus:
            if self.tally.LAP > 0:
                self.tally.LAP -= 1
            self.lapTally.setText(f"{self.tally.LAP}")
        if button == TimerPushButtons.LAP_plus:
            self.tally.LAP += 1
            self.lapTally.setText(f"{self.tally.LAP}")
    
    def PlayPause(self):
        if self.count != 0:
            if self.start:
                self.start = False
                self.startPauseButton.setIcon(QIcon(Images.play))
            else:
                self.start = True
                self.startPauseButton.setIcon(QIcon(Images.pause))
        else:
            self.SetTimerDialog()

    def EndSession(self):
        self.start = False
        self.count = 0
        self.startPauseButton.setIcon(QIcon(Images.play))
        # Save the data to dashboard 
        self.saveData.emit(self.tally)
        self.timeLabel.setText("Session ended")

    def UpdateTime(self):
        if self.start:
            self.count -= 1
            
            if self.count == 0:
                self.timeLabel.setText("Time's up!")
                self.start = False
                self.startPauseButton.setIcon(QIcon(Images.play))

                self.saveData.emit(self.tally)

            else:
                self.timeLabel.setText(f"{timedelta(seconds=self.count)}")


    def SetTimerDialog(self):
        self.start = False
        self.startPauseButton.setIcon(QIcon(Images.play))

        self.timerInputDialog = TimerDialog(self.parent().parent())
        if self.timerInputDialog.exec():
            self.count = self.timerInputDialog.spinBox.value() * 60
            self.timeLabel.setText(f"{timedelta(seconds=self.count)}")
            self.ResetLabels()
        
            
    def ResetLabels(self):
        self.callsTally.setText("0")
        self.connectsTally.setText("0")
        self.bapTally.setText("0")
        self.mapTally.setText("0")
        self.lapTally.setText("0")
