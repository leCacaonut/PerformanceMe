"""Settings tab"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot

from constants import Tally

class DashboardWidget(QWidget):
    callSessions = 0
    calls = 0
    connects = 0
    appointments = 0

    def __init__(self, parent):
        super(DashboardWidget, self).__init__(parent)
        # Define a layout to use
        self.layout = QGridLayout(self)

        # Create widgets
        self.button1 = QPushButton("But1", self)
        self.button2 = QPushButton("But2", self)
        self.label = QLabel("LABEL", self)

        # Add widgets
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.label)

    @pyqtSlot(Tally)
    def UpdateTally(self, tally):
        self.callSessions += 1
        if isinstance(tally, Tally):
            self.calls += tally.calls
            self.connects += tally.connects
            self.appointments += tally.BAP + tally.MAP + tally.LAP
