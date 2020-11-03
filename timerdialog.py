"""GUI"""

from PyQt5.QtWidgets import QInputDialog

class TimerDialog(QInputDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.number, self.ok = self.getInt(self, "Set timer", "Enter number of minutes", value=45)
        self.number *= 60
