"""Dashboard tab"""

import os
import json
import uuid

from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QToolButton, QLabel, QSizePolicy, QFrame
from PyQt5.QtCore import pyqtSlot, QSize, Qt, QStandardPaths, QDate
from PyQt5.QtGui import QIcon

from constants import default_icon_size, uuid_namespace, Tally, Images, ActionType

from customsubclasses import StretchedLabel, CustomToolButton
from dashboardpopup import DashboardAdd, DashboardSetGoal

class DashboardWidget(QWidget):
    monthView = False
    addview = None
    goaldialog = None

    def __init__(self, parent):
        super().__init__(parent)
        self.dataParent = parent.parent()

        # Define a layout to use
        self.layoutBase = QVBoxLayout(self)
        self.layoutTop = QGridLayout()
        self.layoutBottom = QGridLayout()

        # self.LoadData()

        # Create widgets
        # First section
        self.nAppraisals = QLabel(self)
        self.lAppraisals = QLabel("Appraisals", self)
        self.iAppraisals = CustomToolButton(self)
        self.nListings = QLabel(self)
        self.lListings = QLabel("Listings", self)
        self.iListings = CustomToolButton(self)
        self.nSales = QLabel(self)
        self.lSales = QLabel("Sales", self)
        self.iSales = CustomToolButton(self)
        self.nIncome = QLabel(self)
        self.lIncome = QLabel("Income", self)
        self.iIncome = CustomToolButton(self)


        # Second section
        self.lCallSessions = StretchedLabel("Call Sessions", self)
        self.nCallSessions = StretchedLabel(self)
        self.lCalls = StretchedLabel("Calls", self)
        self.nCalls = StretchedLabel(self)
        self.lConnects = StretchedLabel("Connects", self)
        self.nConnects = StretchedLabel(self)
        self.lConnectsRatio = StretchedLabel("Connects Ratio", self)
        self.nConnectsRatio = StretchedLabel(self)
        self.lAppointments = StretchedLabel("Appointments", self)
        self.nAppointments = StretchedLabel(self)
        self.bQuit = QToolButton(self)


        # Widget configuration
        # Top
        self.nAppraisals.setWordWrap(True)
        self.nAppraisals.setAlignment(Qt.AlignCenter)
        self.lAppraisals.setAlignment(Qt.AlignCenter)
        self.lAppraisals.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.iAppraisals.setIcon(QIcon(Images.plus))
        self.iAppraisals.setText("Add appraisal")
        self.iAppraisals.clicked.connect(lambda: self.AddAction(ActionType.appraisal))

        self.nListings.setWordWrap(True)
        self.nListings.setAlignment(Qt.AlignCenter)
        self.lListings.setAlignment(Qt.AlignCenter)
        self.lListings.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.iListings.setIcon(QIcon(Images.plus))
        self.iListings.setText("Add listing")
        self.iListings.clicked.connect(lambda: self.AddAction(ActionType.listing))

        self.nSales.setWordWrap(True)
        self.nSales.setAlignment(Qt.AlignCenter)
        self.lSales.setAlignment(Qt.AlignCenter)
        self.lSales.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.iSales.setIcon(QIcon(Images.plus))
        self.iSales.setText("Add sale")
        self.iSales.clicked.connect(lambda: self.AddAction(ActionType.sale))

        self.nIncome.setWordWrap(True)
        self.nIncome.setAlignment(Qt.AlignCenter)
        self.lIncome.setAlignment(Qt.AlignCenter)
        self.lIncome.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.iIncome.setIcon(QIcon(Images.hamburger))
        self.iIncome.setText("Set goals")
        self.iIncome.clicked.connect(self.SetGoals)
        
        # Bottom
        self.lCallSessions.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.lCallSessions.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.nCallSessions.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.nCallSessions.setStyleSheet("font-size: 40px;")
        self.lCalls.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.lCalls.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.nCalls.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.nCalls.setStyleSheet("font-size: 40px;")
        self.lConnects.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.lConnects.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.nConnects.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.nConnects.setStyleSheet("font-size: 40px;")
        self.lConnectsRatio.setWordWrap(True)
        self.lConnectsRatio.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.lConnectsRatio.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.nConnectsRatio.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.nConnectsRatio.setStyleSheet("font-size: 40px;")
        self.lAppointments.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.lAppointments.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.nAppointments.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.nAppointments.setStyleSheet("font-size: 40px;")
        
        self.bQuit.setIcon(QIcon(Images.exit))
        self.bQuit.setIconSize(QSize(default_icon_size, default_icon_size))
        self.bQuit.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.bQuit.setText("Save && exit")

        # self.lCallSessions.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        # self.nCallSessions.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.lCalls.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        # self.nCalls.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.lConnects.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        # self.nConnects.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.lConnectsRatio.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        # self.nConnectsRatio.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.lAppointments.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        # self.nAppointments.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        # self.bQuit.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))

        # Setup buttons
        # self.bQuit.clicked.connect(self.SwitchViews)
        self.bQuit.clicked.connect(self.parent().parent().close)

        # Add widgets
        self.layoutTop.addWidget(self.nAppraisals, 0, 0)
        self.layoutTop.addWidget(self.lAppraisals, 1, 0)
        self.layoutTop.addWidget(self.iAppraisals, 2, 0)
        self.layoutTop.addWidget(self.nListings, 0, 1)
        self.layoutTop.addWidget(self.lListings, 1, 1)
        self.layoutTop.addWidget(self.iListings, 2, 1)
        self.layoutTop.addWidget(self.nSales, 0, 2)
        self.layoutTop.addWidget(self.lSales, 1, 2)
        self.layoutTop.addWidget(self.iSales, 2, 2)
        self.layoutTop.addWidget(self.nIncome, 0, 3)
        self.layoutTop.addWidget(self.lIncome, 1, 3)
        self.layoutTop.addWidget(self.iIncome, 2, 3)
        self.layoutBase.addLayout(self.layoutTop)

        # Add a separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layoutBase.addWidget(sep)

        self.layoutBottom.addWidget(self.lCallSessions, 0, 0)
        self.layoutBottom.addWidget(self.nCallSessions, 1, 0)
        self.layoutBottom.addWidget(self.lCalls, 0, 1)
        self.layoutBottom.addWidget(self.nCalls, 1, 1)
        self.layoutBottom.addWidget(self.lConnects, 2, 0)
        self.layoutBottom.addWidget(self.nConnects, 3, 0)
        self.layoutBottom.addWidget(self.lConnectsRatio, 2, 1)
        self.layoutBottom.addWidget(self.nConnectsRatio, 3, 1)
        self.layoutBottom.addWidget(self.lAppointments, 4, 0)
        self.layoutBottom.addWidget(self.nAppointments, 5, 0)
        self.layoutBottom.addWidget(self.bQuit, 4, 1, 2, 1, alignment=Qt.AlignHCenter)
        self.layoutBase.addLayout(self.layoutBottom)

        self.layoutBottom.setColumnStretch(0, 3)
        self.layoutBottom.setColumnStretch(1, 2)
        self.layoutBase.setStretch(0, 2)
        self.layoutBase.setStretch(1, 0)
        self.layoutBase.setStretch(2, 3)
        
    @pyqtSlot(ActionType, str, QDate)
    @pyqtSlot(ActionType, str, QDate, int, float)
    def UpdateDashboard(self, actionType, address, date, price=0, commission=0):
        #pylint: disable=too-many-arguments
        date = date.toString('yyyy/MM/dd')
        a_uuid = f"{uuid.uuid5(uuid_namespace, address)}"
        # If uuid already exists in the list, use it
        if a_uuid in self.dataParent.propertyData:
            data = self.dataParent.propertyData[a_uuid]
        # Otherwise, create a new address
        else:
            data = {'address': address}

        if actionType is ActionType.appraisal:
            data |= {'appraisal_date': date}
        elif actionType is ActionType.listing:
            data |= {'listing_date': date}
        elif actionType is ActionType.sale:
            data |= {'sale_date': date, 'price': price, 'commission': commission}
        
        self.dataParent.propertyData |= {a_uuid: data}
        self.dataParent.UpdateDataCount()

        self.UpdateText()

    @pyqtSlot(int, int, int, int)
    def UpdateDashboardGoal(self, appraisalGoal, listingGoal, saleGoal, incomeGoal):
        self.dataParent.appraisalGoal = appraisalGoal
        self.dataParent.listingGoal = listingGoal
        self.dataParent.saleGoal = saleGoal
        self.dataParent.incomeGoal = incomeGoal
        
        self.UpdateText()

    @pyqtSlot(Tally)
    def UpdateTally(self, tally):
        self.dataParent.callSessions += 1
        if isinstance(tally, Tally):
            self.dataParent.calls += tally.calls
            self.dataParent.connects += tally.connects
            self.dataParent.appointments += tally.BAP + tally.MAP + tally.LAP

        self.UpdateText()

    def UpdateText(self):
        self.nAppraisals.setText(f"{self.dataParent.appraisals} \n/ {self.dataParent.appraisalGoal}")
        self.nListings.setText(f"{self.dataParent.listings} \n/ {self.dataParent.listingGoal}")
        self.nSales.setText(f"{self.dataParent.sales} \n/ {self.dataParent.saleGoal}")
        self.nIncome.setText("$ " + f"{self.dataParent.income:,.0f} \n/ {self.dataParent.incomeGoal:,.0f}")

        self.nCallSessions.setText(f"{self.dataParent.callSessions}")
        self.nCalls.setText(f"{self.dataParent.calls}")
        self.nConnects.setText(f"{self.dataParent.connects}")
        connectsRatio = 0
        if self.dataParent.calls != 0:
            connectsRatio = self.dataParent.connects / self.dataParent.calls
        self.nConnectsRatio.setText(f"{connectsRatio:.2f}")
        self.nAppointments.setText(f"{self.dataParent.appointments}")

        # Set text colours
        if self.dataParent.appraisals >= self.dataParent.appraisalGoal:
            self.nAppraisals.setStyleSheet("color: #0fd444; font-size: 26px;")
        else:
            self.nAppraisals.setStyleSheet("font-size: 26px;")
        if self.dataParent.listings >= self.dataParent.listingGoal:
            self.nListings.setStyleSheet("color: #0fd444; font-size: 26px;")
        else:
            self.nListings.setStyleSheet("font-size: 26px;")
        if self.dataParent.sales >= self.dataParent.saleGoal:
            self.nSales.setStyleSheet("color: #0fd444; font-size: 26px;")
        else:
            self.nSales.setStyleSheet("font-size: 26px;")
        if self.dataParent.income >= self.dataParent.incomeGoal:
            self.nIncome.setStyleSheet("color: #0fd444; font-size: 26px;")
        else:
            self.nIncome.setStyleSheet("font-size: 26px;")

    def AddAction(self, actionType):
        self.addview = DashboardAdd(parent=self.parent().parent(), actionType=actionType)
        self.addview.okPressed[ActionType, str, QDate].connect(self.UpdateDashboard)
        self.addview.okPressed[ActionType, str, QDate, int, float].connect(self.UpdateDashboard)
        self.addview.show()
        # Don't need to exec()
        # self.addview.exec()

    def SetGoals(self):
        self.goaldialog = DashboardSetGoal(self.dataParent.appraisalGoal, self.dataParent.listingGoal, self.dataParent.saleGoal, self.dataParent.incomeGoal, parent=self.parent().parent())
        self.goaldialog.okPressed.connect(self.UpdateDashboardGoal)
