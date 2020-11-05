"""
Dashboard window
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QDateEdit, QLabel, QSizePolicy, QSpinBox, QLineEdit, QDoubleSpinBox, QMessageBox, QDialogButtonBox, QApplication
from PyQt5.QtCore import Qt, QDate, QPoint, pyqtSignal, QSize, QMargins

from constants import ActionType, motivational_string

class DashboardAdd(QDialog):
    okPressed = pyqtSignal([ActionType, str, QDate], [ActionType, str, QDate, int, float])

    def __init__(self, parent=None, actionType=ActionType.appraisal):
        super().__init__()
        self.setWindowTitle("Enter details")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setContentsMargins(QMargins(3, 3, 3, 3))
        self.setStyleSheet("font-size: 20px")

        self.actionType = actionType

        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.titleDescription = QLabel(self)
        self.addressLabel = QLabel("Enter address:", self)
        self.addressInput = QLineEdit(self)
        self.dateLabel = QLabel("Enter date:", self)
        self.dateInput = QDateEdit(QDate.currentDate(), self)

        self.dialogButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialogButtons.accepted.connect(self.SendDataToDashboard)
        # self.dialogButtons.rejected.connect(self.reject)
        self.dialogButtons.rejected.connect(self.close)
        


        # Widget settings
        self.addressLabel.setAlignment(Qt.AlignBottom)
        self.addressLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.dateLabel.setAlignment(Qt.AlignBottom)
        self.dateLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Set widget layouts
        self.layout.addWidget(self.titleDescription)
        self.layout.addWidget(self.addressLabel)
        self.layout.addWidget(self.addressInput)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dateInput)

        # If this is sale window
        if self.actionType == ActionType.appraisal:
            self.titleDescription.setText("<u><b>Add appraisal</b></u>")
        if self.actionType == ActionType.listing:
            self.titleDescription.setText("<u><b>Add listing</b></u>")
        if self.actionType == ActionType.sale:
            self.titleDescription.setText("<u><b>Add sale</b></u>")
            self.priceLabel = QLabel("Enter price:", self)
            self.priceInput = QSpinBox(self)
            self.commissionLabel = QLabel("Enter commission %:", self)
            self.commissionInput = QDoubleSpinBox(self)

            # Widget setup
            self.priceLabel.setAlignment(Qt.AlignBottom)
            self.priceLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            self.priceInput.setMaximum(100000000)
            self.priceInput.setSingleStep(1000)
            self.priceInput.setValue(1500000)
            self.commissionLabel.setAlignment(Qt.AlignBottom)
            self.commissionLabel.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            self.commissionInput.setMaximum(100)
            self.commissionInput.setSingleStep(0.05)
            self.commissionInput.setValue(2.0)
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
        

    def SendDataToDashboard(self):
        if not self.addressInput.text():
            errormsg = QMessageBox(QMessageBox.Critical, "ERROR", "Address cannot be empty!", QMessageBox.Ok, self)
            errormsg.setWindowFlag(Qt.FramelessWindowHint)
            errormsg.show()
            
        else:
            if self.actionType == ActionType.appraisal or self.actionType == ActionType.listing:
                self.okPressed[ActionType, str, QDate].emit(
                    self.actionType,
                    self.addressInput.text(),
                    self.dateInput.date()
                )
            elif self.actionType == ActionType.sale:
                self.okPressed[ActionType, str, QDate, int, float].emit(
                    self.actionType,
                    self.addressInput.text(),
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
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
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
        self.setAppraisal.setMaximum(99)
        self.setAppraisal.setMinimumSize(QSize(50, 30))
        self.setListing.setValue(listingGoal)
        self.setListing.setMaximum(99)
        self.setListing.setMinimumSize(QSize(50, 30))
        self.setSale.setValue(saleGoal)
        self.setSale.setMaximum(99)
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
