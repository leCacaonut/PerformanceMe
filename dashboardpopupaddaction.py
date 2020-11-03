"""
Dashboard window
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QDateEdit, QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QDate, QPoint, pyqtSignal

from constants import ActionType

class DashboardAdd(QWidget):
    okPressed = pyqtSignal(ActionType, str, QDate)

    def __init__(self, parent=None, actionType=ActionType.appraisal):
        super().__init__()
        p = parent.frameGeometry().topLeft() + parent.rect().center() - self.frameGeometry().center() / 2
        self.move(p)
        self.setWindowTitle("Enter details")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.actionType = actionType

        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.addressLabel = QLabel("Enter address:", self)
        self.addressInput = QLineEdit(self)
        self.dateLabel = QLabel("Enter date:", self)
        self.dateInput = QDateEdit(QDate.currentDate(), self)

        self.ok = QPushButton("OK")
        self.ok.clicked.connect(self.SendDataToDashboard)
        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.close)

        # Widget settings
        self.addressLabel.setAlignment(Qt.AlignBottom)
        self.addressLabel.setStyleSheet("font: 16px")
        self.addressLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.dateLabel.setAlignment(Qt.AlignBottom)
        self.dateLabel.setStyleSheet("font: 16px")
        self.dateLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Set widget layouts
        self.layout.addWidget(self.addressLabel)
        self.layout.addWidget(self.addressInput)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dateInput)

        # If this is sale window
        if actionType == ActionType.sale:
            self.saleLabel = QLabel("Enter sale:", self)
            self.saleInput = QLineEdit(self)
            self.commissionLabel = QLabel("Enter commission %:", self)
            self.commissionInput = QLineEdit(self)

            self.saleLabel.setAlignment(Qt.AlignBottom)
            self.saleLabel.setStyleSheet("font: 16px")
            self.saleLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            self.commissionLabel.setAlignment(Qt.AlignBottom)
            self.commissionLabel.setStyleSheet("font: 16px")
            self.commissionLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

            self.layout.addWidget(self.saleLabel)
            self.layout.addWidget(self.saleInput)
            self.layout.addWidget(self.commissionLabel)
            self.layout.addWidget(self.commissionInput)


        self.buttonLayout.addWidget(self.ok)
        self.buttonLayout.addWidget(self.cancel)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

        # self.layout.setStretch(0, 1)
        # self.layout.setStretch(1, 1)
        # self.layout.setStretch(2, 1)
        # self.layout.setStretch(3, 1)
        
        # Setup mouse event handling
        self.oldPos = self.pos()
        
    def SendDataToDashboard(self):
        # print(self.actionType)
        self.okPressed.emit(self.actionType, self.addressInput.text(), self.dateInput.date())
        self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
