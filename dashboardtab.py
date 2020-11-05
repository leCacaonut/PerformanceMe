"""Settings tab"""

import os
import json
import uuid

from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QToolButton, QLabel, QSizePolicy, QFrame
from PyQt5.QtCore import pyqtSlot, QSize, Qt, QStandardPaths, QDate
from PyQt5.QtGui import QIcon

from constants import default_icon_size, data_filename, uuid_namespace, Tally, Images, ActionType

from subclassQLabel import StretchedLabel
from dashboardpopup import DashboardAdd, DashboardSetGoal

class DashboardWidget(QWidget):
    monthView = False
    addview = None
    goaldialog = None

    # Use common parent to transfer data
    # appraisalData = {}
    # listingData = {}
    # saleData = {}

    appraisals = 0
    listings = 0
    sales = 0
    income = 0

    appraisalGoal = 2
    listingGoal = 1
    saleGoal = 1
    incomeGoal = 50000

    callSessions = 0
    calls = 0
    connects = 0
    connectsRatio = 0
    appointments = 0

    def __init__(self, parent):
        super().__init__(parent)
        # Define a layout to use
        self.layoutBase = QVBoxLayout(self)
        self.layoutTop = QGridLayout()
        self.layoutBottom = QGridLayout()

        self.LoadData()

        # Create widgets
        # First section
        self.nAppraisals = QLabel(self)
        self.lAppraisals = QLabel("Appraisals", self)
        self.nListings = QLabel(self)
        self.lListings = QLabel("Listings", self)
        self.nSales = QLabel(self)
        self.lSales = QLabel("Sales", self)
        self.nIncome = QLabel(self)
        self.lIncome = QLabel("Income", self)

        self.iAppraisals = QToolButton(self)
        self.iListings = QToolButton(self)
        self.iSales = QToolButton(self)
        self.iIncome = QToolButton(self)

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
        self.bSwitchTimeline = QToolButton(self)


        # Widget configuration
        # Top
        self.nAppraisals.setWordWrap(True)
        self.nAppraisals.setStyleSheet("font-size: 26px;")
        self.lAppraisals.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iAppraisals.setIcon(QIcon(Images.plus))
        self.iAppraisals.setIconSize(QSize(40, 40))
        self.iAppraisals.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iAppraisals.setText("Add appraisal")
        self.iAppraisals.clicked.connect(lambda: self.AddAction(ActionType.appraisal))
        self.nListings.setWordWrap(True)
        self.nListings.setStyleSheet("font-size: 26px;")
        self.lListings.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iListings.setIcon(QIcon(Images.plus))
        self.iListings.setIconSize(QSize(40, 40))
        self.iListings.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iListings.setText("Add listing")
        self.iListings.clicked.connect(lambda: self.AddAction(ActionType.listing))
        self.nSales.setWordWrap(True)
        self.nSales.setStyleSheet("font-size: 26px;")
        self.lSales.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iSales.setIcon(QIcon(Images.plus))
        self.iSales.setIconSize(QSize(40, 40))
        self.iSales.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iSales.setText("Add sale")
        self.iSales.clicked.connect(lambda: self.AddAction(ActionType.sale))
        self.nIncome.setWordWrap(True)
        self.nIncome.setStyleSheet("font-size: 26px;")
        # self.nIncome.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        self.lIncome.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iIncome.setIcon(QIcon(Images.hamburger))
        self.iIncome.setIconSize(QSize(40, 40))
        self.iIncome.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iIncome.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred))
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
        
        self.bSwitchTimeline.setIcon(QIcon(Images.exit))
        self.bSwitchTimeline.setIconSize(QSize(default_icon_size, default_icon_size))
        self.bSwitchTimeline.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.bSwitchTimeline.setText("Save && exit")

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
        # self.bSwitchTimeline.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))

        # Setup buttons
        # self.bSwitchTimeline.clicked.connect(self.SwitchViews)
        self.bSwitchTimeline.clicked.connect(self.parent().parent().close)

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
        self.layoutBottom.addWidget(self.bSwitchTimeline, 4, 1, 2, 1, alignment=Qt.AlignHCenter)
        self.layoutBase.addLayout(self.layoutBottom)

        self.layoutBottom.setColumnStretch(0, 3)
        self.layoutBottom.setColumnStretch(1, 2)
        self.layoutBase.setStretch(0, 2)
        self.layoutBase.setStretch(1, 0)
        self.layoutBase.setStretch(2, 3)
        
        self.UpdateText()
        
    def LoadData(self):
        if not os.path.exists(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)):
            os.makedirs(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
        try:
            with open(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_filename, 'r') as file:
                try:
                    jsonData = json.load(file)
                    # Default values are already set at start of class
                    self.parent().parent().appraisalData = jsonData.get('appraisaldata', self.parent().parent().appraisalData)
                    self.parent().parent().listingData = jsonData.get('listingdata', self.parent().parent().listingData)
                    self.parent().parent().saleData = jsonData.get('saledata', self.parent().parent().saleData)
                    
                    self.appraisalGoal = jsonData.get('appraisalgoal', self.appraisalGoal)
                    self.listingGoal = jsonData.get('listinggoal', self.listingGoal)
                    self.saleGoal = jsonData.get('salegoal', self.saleGoal)
                    self.incomeGoal = jsonData.get('incomegoal', self.incomeGoal)
                    self.callSessions = jsonData.get('call_sessions', self.callSessions)
                    self.calls = jsonData.get('calls', self.calls)
                    self.connects = jsonData.get('connects', self.connects)
                    self.appointments = jsonData.get('appointments', self.appointments)
                
                except json.JSONDecodeError as e:
                    print(e)

                # for data in self.parent().parent().appraisalData:
                #     print(self.parent().parent().appraisalData[data])
                # for data in self.parent().parent().listingData:
                #     print(self.parent().parent().listingData[data])
                # for data in self.parent().parent().saleData:
                #     print(self.parent().parent().saleData[data])
                
        except FileNotFoundError as e:
            print(e)

    def SaveData(self):
        print("Saving data...")
        data = {'appraisaldata': self.parent().parent().appraisalData,
            'listingdata': self.parent().parent().listingData,
            'saledata': self.parent().parent().saleData,
            'income': self.income,
            'appraisalgoal': self.appraisalGoal,
            'listinggoal': self.listingGoal,
            'salegoal': self.saleGoal,
            'incomegoal': self.incomeGoal,
            'call_sessions': self.callSessions,
            'calls': self.calls,
            'connects': self.connects,
            'appointments': self.appointments}

        with open(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_filename, 'w+') as file:
            json.dump(data, file, indent=4)

    @pyqtSlot(ActionType, str, QDate)
    @pyqtSlot(ActionType, str, QDate, int, float)
    def UpdateDashboard(self, actionType, address, date, price=0, commission=0):
        #pylint: disable=too-many-arguments
        date = date.toString('dd/MM/yyyy')
        if actionType == ActionType.appraisal:
            self.parent().parent().appraisalData |= {str(uuid.uuid5(uuid_namespace, address)): {'address': address, 'date': date}}
        elif actionType == ActionType.listing:
            self.parent().parent().listingData |= {str(uuid.uuid5(uuid_namespace, address)): {'address': address, 'date': date}}
        elif actionType == ActionType.sale:
            self.parent().parent().saleData |= {str(uuid.uuid5(uuid_namespace, address)): {'address': address, 'date': date, 'price': price, 'commission': commission}}

        self.UpdateText()

    @pyqtSlot(int, int, int, int)
    def UpdateDashboardGoal(self, appraisalGoal, listingGoal, saleGoal, incomeGoal):
        self.appraisalGoal = appraisalGoal
        self.listingGoal = listingGoal
        self.saleGoal = saleGoal
        self.incomeGoal = incomeGoal
        
        self.UpdateText()

    @pyqtSlot(Tally)
    def UpdateTally(self, tally):
        self.callSessions += 1
        if isinstance(tally, Tally):
            self.calls += tally.calls
            self.connects += tally.connects
            self.appointments += tally.BAP + tally.MAP + tally.LAP

        self.UpdateText()

    def UpdateText(self):
        self.appraisals = len(self.parent().parent().appraisalData)
        self.listings = len(self.parent().parent().listingData)
        self.sales = len(self.parent().parent().saleData)
        self.income = 0
        for data in self.parent().parent().saleData:
            self.income += self.parent().parent().saleData[data]['price'] * self.parent().parent().saleData[data]['commission'] / 100

        self.nAppraisals.setText(str(self.appraisals) + "\n/ " + str(self.appraisalGoal))
        self.nListings.setText(str(self.listings) + "\n/ " + str(self.listingGoal))
        self.nSales.setText(str(self.sales) + "\n/ " + str(self.saleGoal))
        self.nIncome.setText("$ " + f"{int(self.income):,}" + "\n/ " + f"{int(self.incomeGoal):,}")

        self.nCallSessions.setText(str(self.callSessions))
        self.nCalls.setText(str(self.calls))
        self.nConnects.setText(str(self.connects))
        if self.calls != 0:
            self.connectsRatio = self.connects / self.calls
        self.nConnectsRatio.setText(f"{self.connectsRatio:.2f}")
        self.nAppointments.setText(str(self.appointments))

        # Set text colours
        if self.appraisals >= self.appraisalGoal:
            self.nAppraisals.setStyleSheet("color: #0fd444; font-size: 26px;")
        else:
            self.nAppraisals.setStyleSheet("font-size: 26px;")
        if self.listings >= self.listingGoal:
            self.nListings.setStyleSheet("color: #0fd444; font-size: 26px;")
        else:
            self.nListings.setStyleSheet("font-size: 26px;")
        if self.sales >= self.saleGoal:
            self.nSales.setStyleSheet("color: #0fd444; font-size: 26px;")
        else:
            self.nSales.setStyleSheet("font-size: 26px;")
        if self.income >= self.incomeGoal:
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
        self.goaldialog = DashboardSetGoal(self.appraisalGoal, self.listingGoal, self.saleGoal, self.incomeGoal, parent=self.parent().parent())
        self.goaldialog.okPressed.connect(self.UpdateDashboardGoal)
    
    def closeEvent(self, _):
        self.SaveData()
