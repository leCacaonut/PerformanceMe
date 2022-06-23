"""Detail editing"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDateEdit, QLabel, QSpinBox, QLineEdit, QDoubleSpinBox, QDialogButtonBox
from PyQt5.QtCore import Qt, QDate, QPoint, pyqtSignal, QMargins, QVariant
from PyQt5.QtGui import QIcon

from constants import ActionType

class DetailEdit(QDialog):
    okPressed = pyqtSignal(
        [ActionType, QVariant, dict, QDate],
        [ActionType, QVariant, dict, QDate, int, float]
    )
    
    def __init__(self, actionType, a_uuid, address, date, price=1500000, commission=2, parent=None):
        super().__init__()

        self.setWindowTitle("Edit details")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images/hamburger.png'))
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        self.dataParent = parent
        self.actionType = actionType
        self.a_uuid = a_uuid
        self.address = address

        self.layout = QVBoxLayout(self)
        self.addressLayout = QHBoxLayout()

        self.titleDescription = QLabel(self)
        self.addressLabel = QLabel("Address:", self)
        self.addressInputSuburb = QLineEdit(address['suburb'], self)
        self.addressInputPostcode = QLineEdit(address['postcode'], self)
        self.addressInputStreet = QLineEdit(address['street'], self)
        self.addressInputNumber = QLineEdit(address['number'], self)
        self.dateLabel = QLabel("Enter date:", self)
        self.dateInput = QDateEdit(date, self)

        # self.addressInput.setText(self.address)
        # self.addressInput.setReadOnly(True)

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
        self.addressLayout.addWidget(self.addressInputSuburb)
        self.addressLayout.addWidget(self.addressInputPostcode)
        self.layout.addLayout(self.addressLayout)
        self.layout.addWidget(self.addressInputStreet)
        self.layout.addWidget(self.addressInputNumber)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dateInput)

        self.addressLayout.setStretch(0, 2)
        self.addressLayout.setStretch(1, 1)
        
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

        self.setLayout(self.layout)
        
        # Move window calculations correctly
        self.show()
        self.move(int(parent.frameGeometry().center().x() - self.frameGeometry().width() / 2), int(parent.frameGeometry().center().y() - self.frameGeometry().height() / 2))
        # Setup mouse event handling
        self.oldPos = self.pos()

    def UpdateItem(self):
        address = {'address': {
            'suburb': " ".join(self.addressInputSuburb.text().split()),
            'postcode': "".join(self.addressInputPostcode.text().split()),
            'street': " ".join(self.addressInputStreet.text().split()),
            'number': "".join(self.addressInputNumber.text().split())
        }}
        if self.actionType is ActionType.appraisal or self.actionType is ActionType.listing:
            self.okPressed[ActionType, QVariant, dict, QDate].emit(
                self.actionType,
                self.a_uuid,
                address,
                self.dateInput.date()
            )
        elif self.actionType is ActionType.sale:
            self.okPressed[ActionType, QVariant, dict, QDate, int, float].emit(
                self.actionType,
                self.a_uuid,
                address,
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
    okPressed = pyqtSignal(
        [ActionType, QVariant, QDate],
        [ActionType, QVariant, QDate, int, float]
    )
    
    def __init__(self, actionType, a_uuid, address, date, price=1500000, commission=2, parent=None):
        super().__init__()

        self.setWindowTitle("Convert details")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images/hamburger.png'))
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        self.dataParent = parent
        self.actionType = actionType
        self.a_uuid = a_uuid
        self.address = address

        self.layout = QVBoxLayout(self)
        self.addressLayout = QHBoxLayout()

        self.titleDescription = QLabel(self)
        self.addressLabel = QLabel("Address:", self)
        self.addressInputSuburb = QLineEdit(address['suburb'], self)
        self.addressInputPostcode = QLineEdit(address['postcode'], self)
        self.addressInputStreet = QLineEdit(address['street'], self)
        self.addressInputNumber = QLineEdit(address['number'], self)
        self.dateLabel = QLabel("Enter date:", self)
        self.dateInput = QDateEdit(date, self)

        # self.addressInput.setText(self.address)
        # self.addressInput.setReadOnly(True)

        self.dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.UpdateItem)
        # self.dialogButtons.rejected.connect(self.reject)
        self.dialogButtons.rejected.connect(self.close)
        
        # Widget settings
        self.addressLabel.setAlignment(Qt.AlignBottom)
        self.dateLabel.setAlignment(Qt.AlignBottom)
        self.addressInputSuburb.setReadOnly(True) 
        self.addressInputPostcode.setReadOnly(True)
        self.addressInputStreet.setReadOnly(True)
        self.addressInputNumber.setReadOnly(True)

        # Set widget layouts
        self.layout.addWidget(self.titleDescription)
        self.layout.addWidget(self.addressLabel)
        self.addressLayout.addWidget(self.addressInputSuburb)
        self.addressLayout.addWidget(self.addressInputPostcode)
        self.layout.addLayout(self.addressLayout)
        self.layout.addWidget(self.addressInputStreet)
        self.layout.addWidget(self.addressInputNumber)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dateInput)

        self.addressLayout.setStretch(0, 2)
        self.addressLayout.setStretch(1, 1)

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

        self.setLayout(self.layout)

        # Move window calculations correctly
        self.show()
        self.move(int(parent.frameGeometry().center().x() - self.frameGeometry().width() / 2), int(parent.frameGeometry().center().y() - self.frameGeometry().height() / 2))
        # Setup mouse event handling
        self.oldPos = self.pos()

    def UpdateItem(self):
        if self.actionType is ActionType.appraisal:
            self.okPressed[ActionType, QVariant, QDate].emit(
                self.actionType,
                self.a_uuid,
                self.dateInput.date()
            )
        elif self.actionType is ActionType.listing:
            self.okPressed[ActionType, QVariant, QDate, int, float].emit(
                self.actionType,
                self.a_uuid,
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
