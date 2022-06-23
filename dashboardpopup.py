"""Dashboard window"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QDateEdit, QLabel, QSpinBox, QLineEdit, QDoubleSpinBox, QMessageBox, QDialogButtonBox
from PyQt5.QtCore import Qt, QDate, QPoint, pyqtSignal, QSize, QMargins, QVariant
from PyQt5.QtGui import QIcon

from constants import ActionType, motivational_string

class DashboardAdd(QDialog):
    okPressed = pyqtSignal(
        [ActionType, QVariant, str, str, str, str, QDate],
        [ActionType, QVariant, str, str, str, str, QDate, int, float]
    )

    def __init__(self, parent=None, actionType=ActionType.appraisal):
        super().__init__()
        self.setWindowTitle("Enter details")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images/plus.png'))
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        self.dataParent = parent
        self.actionType = actionType

        self.layout = QVBoxLayout(self)
        self.addressLayout = QHBoxLayout()

        self.titleDescription = QLabel(self)
        self.addressLabel = QLabel("Enter address:", self)
        self.addressInputSuburb = QLineEdit("SUBURB", self)
        self.addressInputPostcode = QLineEdit("P/CODE", self)
        self.addressInputStreet = QLineEdit("STREET", self)
        self.addressInputNumber = QLineEdit("NUMBER", self)
        self.dateLabel = QLabel("Enter date:", self)
        self.dateInput = QDateEdit(QDate.currentDate(), self)

        self.dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.SendDataToDashboard)
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

        # Change text based on action type
        if self.actionType is ActionType.appraisal:
            self.titleDescription.setText("<u><b>Add appraisal</b></u>")
        if self.actionType is ActionType.listing:
            self.titleDescription.setText("<u><b>Add listing</b></u>")
        if self.actionType is ActionType.sale:
            self.titleDescription.setText("<u><b>Add sale</b></u>")
            self.priceLabel = QLabel("Enter price:", self)
            self.priceInput = QSpinBox(self)
            self.commissionLabel = QLabel("Enter commission %:", self)
            self.commissionInput = QDoubleSpinBox(self)

            # Widget setup
            self.priceLabel.setAlignment(Qt.AlignBottom)
            self.priceInput.setMaximum(100000000)
            self.priceInput.setSingleStep(1000)
            self.priceInput.setValue(1500000)
            self.commissionLabel.setAlignment(Qt.AlignBottom)
            self.commissionInput.setMaximum(100)
            self.commissionInput.setSingleStep(0.05)
            self.commissionInput.setValue(2.0)
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
        

    def SendDataToDashboard(self):
        a_uuid = None
        for data in self.dataParent.propertyData:
            if (
                " ".join(self.addressInputSuburb.text().split()) in self.dataParent.propertyData[data]['address'].values() and \
                "".join(self.addressInputPostcode.text().split()) in self.dataParent.propertyData[data]['address'].values() and \
                " ".join(self.addressInputStreet.text().split()) in self.dataParent.propertyData[data]['address'].values() and \
                "".join(self.addressInputNumber.text().split()) in self.dataParent.propertyData[data]['address'].values()
            ):
                if (
                    self.actionType is ActionType.appraisal and 'appraisal_date' in self.dataParent.propertyData[data] or \
                    self.actionType is ActionType.listing and 'listing_date' in self.dataParent.propertyData[data] or \
                    self.actionType is ActionType.sale and 'sale_date' in self.dataParent.propertyData[data] \
                ):
                    errormsg = QMessageBox(QMessageBox.Critical, "ERROR", "Address already exists!", QMessageBox.Ok, self)
                    errormsg.setWindowFlag(Qt.FramelessWindowHint)
                    errormsg.show()
                    return
                else:
                    a_uuid = data
                

        if (not self.addressInputSuburb.text() or
            not self.addressInputPostcode.text() or
            not self.addressInputStreet.text() or
            not self.addressInputNumber.text()
        ):
            errormsg = QMessageBox(QMessageBox.Critical, "ERROR", "All forms must be filled!", QMessageBox.Ok, self)
            errormsg.setWindowFlag(Qt.FramelessWindowHint)
            errormsg.show()
            
        else:
            if self.actionType is ActionType.appraisal or self.actionType is ActionType.listing:
                self.okPressed[ActionType, QVariant, str, str, str, str, QDate].emit(
                    self.actionType,
                    a_uuid,
                    " ".join(self.addressInputSuburb.text().split()),
                    "".join(self.addressInputPostcode.text().split()),
                    " ".join(self.addressInputStreet.text().split()),
                    "".join(self.addressInputNumber.text().split()),
                    self.dateInput.date()
                )
            elif self.actionType is ActionType.sale:
                self.okPressed[ActionType, QVariant, str, str, str, str, QDate, int, float].emit(
                    self.actionType,
                    a_uuid,
                    " ".join(self.addressInputSuburb.text().split()),
                    "".join(self.addressInputPostcode.text().split()),
                    " ".join(self.addressInputStreet.text().split()),
                    "".join(self.addressInputNumber.text().split()),
                    self.dateInput.date(),
                    self.priceInput.value(),
                    self.commissionInput.value()
                )
            
            # We do nothing with the signal
            # self.accept()
            self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.oldPos = event.globalPos()

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Return:
    #         self.SendDataToDashboard()
    #     elif event.key() == Qt.Key_Escape:
    #         self.close()


class DashboardSetGoal(QDialog):
    okPressed = pyqtSignal(int, int, int, int)
    def __init__(self, appraisalGoal, listingGoal, saleGoal, incomeGoal, parent=None):
        super().__init__()
        self.setWindowTitle("Set goals")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QIcon('images/hamburger.png'))
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        # Setup
        self.layout = QFormLayout(self)
        self.appraisal = QLabel("Appraisal goal")
        self.setAppraisal = QSpinBox(self)
        self.listing = QLabel("Listing goal")
        self.setListing = QSpinBox(self)
        self.sale = QLabel("Sale goal")
        self.setSale = QSpinBox(self)
        self.income = QLabel("Income goal")
        self.setIncome = QSpinBox(self)

        self.dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.SendDataToDashboard)
        # self.dialogButtons.rejected.connect(self.reject)
        self.dialogButtons.rejected.connect(self.close)

        # Configuration
        self.setAppraisal.setValue(appraisalGoal)
        self.setAppraisal.setMaximum(999)
        self.setAppraisal.setMinimumSize(QSize(50, 30))
        self.setListing.setValue(listingGoal)
        self.setListing.setMaximum(999)
        self.setListing.setMinimumSize(QSize(50, 30))
        self.setSale.setValue(saleGoal)
        self.setSale.setMaximum(999)
        self.setSale.setMinimumSize(QSize(50, 30))
        self.setIncome.setSingleStep(1000)
        self.setIncome.setMaximum(100000000)
        self.setIncome.setValue(incomeGoal)
        self.setIncome.setMinimumSize(QSize(50, 30))
        self.setIncome.setProperty("showGroupSeparator", True)

        self.layout.addRow(self.appraisal, self.setAppraisal)
        self.layout.addRow(self.listing, self.setListing)
        self.layout.addRow(self.sale, self.setSale)
        self.layout.addRow(self.income, self.setIncome)
        self.layout.addRow(self.dialogButtons)

        self.setLayout(self.layout)

        # Force gui update
        self.show()
        self.move(parent.frameGeometry().center().x() - self.frameGeometry().width() / 2, parent.frameGeometry().center().y() - self.frameGeometry().height() / 2)
        # Mouse event
        self.oldPos = self.pos()
        
    def SendDataToDashboard(self):
        # print (self.setAppraisal, self.setListing, self.setSale, self.setIncome)
        if self.setAppraisal.value() == 0 or self.setListing.value() == 0 or self.setSale.value() == 0 or self.setIncome.value() == 0:
            errormsg = QMessageBox(QMessageBox.Critical, "ERROR", motivational_string, QMessageBox.Ok, self)
            errormsg.setTextFormat(Qt.RichText)
            errormsg.setWindowFlag(Qt.FramelessWindowHint)
            errormsg.show()
        
        else:
            self.okPressed.emit(self.setAppraisal.value(), self.setListing.value(), self.setSale.value(), self.setIncome.value())
            # We do nothing with the signal
            # self.accept()
            self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        
        self.oldPos = event.globalPos()

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Return:
    #         self.SendDataToDashboard()
    #     elif event.key() == Qt.Key_Escape:
    #         self.close()
