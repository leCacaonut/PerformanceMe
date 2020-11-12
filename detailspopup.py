"""Detail editing"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QDateEdit, QLabel, QSizePolicy, QSpinBox, QLineEdit, QDoubleSpinBox, QMessageBox, QDialogButtonBox
from PyQt5.QtCore import Qt, QDate, QPoint, pyqtSignal, QSize, QMargins

from constants import ActionType, motivational_string

class DetailEdit(QDialog):
    okPressed = pyqtSignal([ActionType, str, QDate], [ActionType, str, QDate, int, float])
    
    def __init__(self, actionType, address, date, price=1500000, commission=2, parent=None):
        super().__init__()

        self.setWindowTitle("Edit details")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        self.dataParent = parent
        self.actionType = actionType
        self.address = address

        self.layout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.titleDescription = QLabel(self)
        self.addressLabel = QLabel("Address:", self)
        self.addressInput = QLineEdit(self)
        self.dateLabel = QLabel("Enter date:", self)
        self.dateInput = QDateEdit(date, self)

        self.addressInput.setText(self.address)
        self.addressInput.setReadOnly(True)

        self.dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.UpdateItem)
        # self.dialogButtons.rejected.connect(self.reject)
        self.dialogButtons.rejected.connect(self.close)
        
        # Widget settings
        self.addressLabel.setAlignment(Qt.AlignBottom)
        self.dateLabel.setAlignment(Qt.AlignBottom)

        # Set widget layouts
        self.layout.addWidget(self.titleDescription)
        self.layout.addWidget(self.addressLabel)
        self.layout.addWidget(self.addressInput)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dateInput)
        
        if self.actionType is ActionType.appraisal:
            self.titleDescription.setText("<u><b>Edit appraisal</b></u>")
        if self.actionType is ActionType.listing:
            self.titleDescription.setText("<u><b>Edit listing</b></u>")
        if self.actionType is ActionType.sale:
            self.titleDescription.setText("<u><b>Edit sale</b></u>")
            self.priceLabel = QLabel("Enter price:", self)
            self.priceInput = QSpinBox(self)
            self.commissionLabel = QLabel("Enter commission %:", self)
            self.commissionInput = QDoubleSpinBox(self)

            # Widget setup
            self.priceLabel.setAlignment(Qt.AlignBottom)
            self.priceInput.setMaximum(100000000)
            self.priceInput.setSingleStep(1000)
            self.priceInput.setValue(price)
            self.commissionLabel.setAlignment(Qt.AlignBottom)
            self.commissionInput.setMaximum(100)
            self.commissionInput.setSingleStep(0.05)
            self.commissionInput.setValue(commission)
            self.priceInput.setProperty("showGroupSeparator", True)

            self.layout.addWidget(self.priceLabel)
            self.layout.addWidget(self.priceInput)
            self.layout.addWidget(self.commissionLabel)
            self.layout.addWidget(self.commissionInput)

        self.layout.addWidget(self.dialogButtons)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)
        
        # Move window calculations correctly
        self.show()
        self.move(parent.frameGeometry().center().x() - self.frameGeometry().width() / 2, parent.frameGeometry().center().y() - self.frameGeometry().height() / 2)
        # Setup mouse event handling
        self.oldPos = self.pos()

    def UpdateItem(self):
        if self.actionType is ActionType.appraisal or self.actionType is ActionType.listing:
            self.okPressed[ActionType, str, QDate].emit(
                self.actionType,
                self.address,
                self.dateInput.date()
            )
        elif self.actionType is ActionType.sale:
            self.okPressed[ActionType, str, QDate, int, float].emit(
                self.actionType,
                self.address,
                self.dateInput.date(),
                self.priceInput.value(),
                self.commissionInput.value()
            )
        self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.oldPos = event.globalPos()
        
class DetailConvert(QDialog):
    okPressed = pyqtSignal([ActionType, str, QDate], [ActionType, str, QDate, int, float])
    
    def __init__(self, actionType, address, date, price=1500000, commission=2, parent=None):
        super().__init__()

        self.setWindowTitle("Convert details")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        self.dataParent = parent
        self.actionType = actionType
        self.address = address

        self.layout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.titleDescription = QLabel(self)
        self.addressLabel = QLabel("Address:", self)
        self.addressInput = QLineEdit(self)
        self.dateLabel = QLabel("Enter date:", self)
        self.dateInput = QDateEdit(date, self)

        self.addressInput.setText(self.address)
        self.addressInput.setReadOnly(True)

        self.dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.UpdateItem)
        # self.dialogButtons.rejected.connect(self.reject)
        self.dialogButtons.rejected.connect(self.close)
        
        # Widget settings
        self.addressLabel.setAlignment(Qt.AlignBottom)
        self.dateLabel.setAlignment(Qt.AlignBottom)

        # Set widget layouts
        self.layout.addWidget(self.titleDescription)
        self.layout.addWidget(self.addressLabel)
        self.layout.addWidget(self.addressInput)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dateInput)

        if self.actionType is ActionType.appraisal:
            self.titleDescription.setText("<u><b>Convert to listing</b></u>")
        if self.actionType is ActionType.listing:
            self.titleDescription.setText("<u><b>Convert to sale</b></u>")
            
            self.priceLabel = QLabel("Enter price:", self)
            self.priceInput = QSpinBox(self)
            self.commissionLabel = QLabel("Enter commission %:", self)
            self.commissionInput = QDoubleSpinBox(self)

            # Widget setup
            self.priceLabel.setAlignment(Qt.AlignBottom)
            self.priceInput.setMaximum(100000000)
            self.priceInput.setSingleStep(1000)
            self.priceInput.setValue(price)
            self.commissionLabel.setAlignment(Qt.AlignBottom)
            self.commissionInput.setMaximum(100)
            self.commissionInput.setSingleStep(0.05)
            self.commissionInput.setValue(commission)
            self.priceInput.setProperty("showGroupSeparator", True)

            self.layout.addWidget(self.priceLabel)
            self.layout.addWidget(self.priceInput)
            self.layout.addWidget(self.commissionLabel)
            self.layout.addWidget(self.commissionInput)

        self.layout.addWidget(self.dialogButtons)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

        # Move window calculations correctly
        self.show()
        self.move(parent.frameGeometry().center().x() - self.frameGeometry().width() / 2, parent.frameGeometry().center().y() - self.frameGeometry().height() / 2)
        # Setup mouse event handling
        self.oldPos = self.pos()

    def UpdateItem(self):
        if self.actionType is ActionType.appraisal:
            self.okPressed[ActionType, str, QDate].emit(
                self.actionType,
                self.address,
                self.dateInput.date()
            )
        elif self.actionType is ActionType.listing:
            self.okPressed[ActionType, str, QDate, int, float].emit(
                self.actionType,
                self.address,
                self.dateInput.date(),
                self.priceInput.value(),
                self.commissionInput.value()
            )
        self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.oldPos = event.globalPos()
