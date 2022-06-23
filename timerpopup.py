"""GUI"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QDoubleSpinBox, QApplication
from PyQt5.QtCore import Qt, QMargins, QPoint
from PyQt5.QtGui import QIcon

class TimerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Set timer")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        self.layout = QVBoxLayout(self)
        
        # Widgets
        self.label = QLabel("Enter time in minutes", self)
        self.spinBox = QDoubleSpinBox(self)
        self.dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.accept)
        self.dialogButtons.rejected.connect(self.reject)
        
        # Configuration
        self.spinBox.setMinimum(0.05)
        self.spinBox.setMaximum(1440)
        self.spinBox.setValue(45)
        self.spinBox.setSingleStep(5)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spinBox)
        self.layout.addWidget(self.dialogButtons)

        self.setLayout(self.layout)

        # Force gui to display correctly
        self.show()
        self.move(int(parent.frameGeometry().center().x() - self.frameGeometry().width() / 2), int(parent.frameGeometry().center().y() - self.frameGeometry().height() / 2))
        # Setup mouse event handling
        self.oldPos = self.pos()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.oldPos = event.globalPos()