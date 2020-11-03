"""Settings tab"""

import os
import json

from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QToolButton, QLabel, QSizePolicy, QFrame
from PyQt5.QtCore import pyqtSlot, QSize, Qt, QStandardPaths, QDate
from PyQt5.QtGui import QIcon

from constants import default_icon_size, data_filename, Tally, Images, ActionType

from subclassQLabel import StretchedLabel
from dashboardpopupaddaction import DashboardAdd
# from dashboardpopupview import 

class DashboardWidget(QWidget):
    monthView = False
    dialog = None

    appraisalData = {}
    listingData = {}
    saleData = {}

    appraisals = 0
    listings = 0
    sales = 0
    income = 0

    appraisalGoal = 2
    listingGoal = 2
    saleGoal = 2
    incomeGoal = 45

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

        self.UpdateText()

        # Widget configuration
        # Top
        self.nAppraisals.setWordWrap(True)
        self.nAppraisals.setStyleSheet("font-size: 26px;")
        self.lAppraisals.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iAppraisals.setIcon(QIcon(Images.plus))
        self.iAppraisals.setIconSize(QSize(40, 40))
        self.iAppraisals.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iAppraisals.setText("Add appraisal")
        self.iAppraisals.clicked.connect(lambda _, x=ActionType.appraisal: self.AddAction(x))
        self.nListings.setWordWrap(True)
        self.nListings.setStyleSheet("font-size: 26px;")
        self.lListings.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iListings.setIcon(QIcon(Images.plus))
        self.iListings.setIconSize(QSize(40, 40))
        self.iListings.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iListings.setText("Add listing")
        self.iListings.clicked.connect(lambda _, x=ActionType.listing: self.AddAction(x))
        self.nSales.setWordWrap(True)
        self.nSales.setStyleSheet("font-size: 26px;")
        self.lSales.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iSales.setIcon(QIcon(Images.plus))
        self.iSales.setIconSize(QSize(40, 40))
        self.iSales.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iSales.setText("Add sale")
        self.iSales.clicked.connect(lambda _, x=ActionType.sale: self.AddAction(x))
        self.nIncome.setWordWrap(True)
        self.nIncome.setStyleSheet("font-size: 26px;")
        self.lIncome.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.iIncome.setIcon(QIcon(Images.plus))
        self.iIncome.setIconSize(QSize(40, 40))
        self.iIncome.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.iIncome.setText("View details")
        self.iIncome.clicked.connect(self.ViewDetails)
        
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
        self.bSwitchTimeline.setText("Exit")

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
        
    def LoadData(self):
        if not os.path.exists(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)):
            os.makedirs(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
        try:
            with open(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_filename, 'r') as file:
                data = json.load(file)
                self.appraisalData = data['appraisaldata']
                self.listingData = data['listingdata']
                self.saleData = data['saledata']
                self.appraisals = data['appraisals']
                self.listings = data['listings']
                self.sales = data['sales']
                self.income = data['income']
                self.callSessions = data['call_sessions']
                self.calls = data['calls']
                self.connects = data['connects']
                self.appointments = data['appointments']


                # TODO: LOAD SETTINGS
                print(self.appraisalData['date'])
                date1 = QDate(QDate.fromString(self.appraisalData['date'], 'dd-MM-yyyy'))
                print(date1)
                # print(self.appraisalData)
                # print(self.listingData)
                # print(self.saleData)
                
        except OSError as e:
            print(e)

    def SaveData(self):
        print("Saving data...")
        data = {{'appraisaldata': self.appraisalData} |
                {'listingdata': self.listingData} |
                {'saledata': self.saleData} |
                {'appraisals': self.appraisals,
                'listings': self.listings,
                'sales': self.sales,
                'income': self.income,
                'call_sessions': self.callSessions,
                'calls': self.calls,
                'connects': self.connects,
                'appointments': self.appointments}}


        with open(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_filename, 'w+') as file:
            json.dump(data, file)

    @pyqtSlot(ActionType, str, QDate)
    def UpdateDashboard(self, actionType, address, date):
        date = date.toString('dd-MM-yyyy')
        if actionType == ActionType.appraisal:
            self.appraisalData |= {'address': address, 'date': date}
        elif actionType == ActionType.listing:
            self.listingData |= {'address': address, 'date': date}
        elif actionType == ActionType.sale:
            self.saleData |= {'address': address, 'date': date}

    @pyqtSlot(Tally)
    def UpdateTally(self, tally):
        self.callSessions += 1
        if isinstance(tally, Tally):
            self.calls += tally.calls
            self.connects += tally.connects
            self.appointments += tally.BAP + tally.MAP + tally.LAP
        self.UpdateText()

    def UpdateText(self):
        self.nAppraisals.setText(str(self.appraisals) + " / " + str(self.appraisalGoal))
        self.nListings.setText(str(self.listings) + " / " + str(self.listingGoal))
        self.nSales.setText(str(self.sales) + " / " + str(self.saleGoal))
        self.nIncome.setText(str(self.income) + " / " + str(self.incomeGoal))

        self.nCallSessions.setText(str(self.callSessions))
        self.nCalls.setText(str(self.calls))
        self.nConnects.setText(str(self.connects))
        if self.calls != 0:
            self.connectsRatio = self.connects / self.calls
        self.nConnectsRatio.setText(f"{self.connectsRatio:.2f}" + "%")
        self.nAppointments.setText(str(self.appointments))


    def AddAction(self, actionType):
        self.dialog = DashboardAdd(self.parent().parent(), actionType)
        self.dialog.okPressed.connect(self.UpdateDashboard)
        self.dialog.show()

    def ViewDetails(self):
        print("View details")
    
    def closeEvent(self, _):
        self.SaveData()
