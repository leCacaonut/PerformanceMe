"""
Dashboard view
"""

import os
import json

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QMenu, QListView
from PyQt5.QtCore import Qt, QStandardPaths

from constants import data_filename, ActionType

class DetailsWidget(QWidget):
    appraisalData = {}
    listingData = {}
    saleData = {}
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.appraisal = QLabel("Appraisals")
        self.appraisal.setStyleSheet("font-size: 18px")
        self.listing = QLabel("Listings")
        self.listing.setStyleSheet("font-size: 18px")
        self.sale = QLabel("Sales")
        self.sale.setStyleSheet("font-size: 18px")

        # List setup
        # Appraisal list
        self.appraisalList = QListWidget(self)
        self.appraisalList.setDragEnabled(True)
        self.appraisalList.setMovement(QListView.Snap)
        self.appraisalList.setDefaultDropAction(Qt.MoveAction)
        self.appraisalList.setSelectionMode(QListWidget.ExtendedSelection)
        self.appraisalList.setStyleSheet("font-size: 14px")

        # Listing list
        self.listingList = QListWidget(self)
        self.listingList.setDragEnabled(True)
        self.listingList.setMovement(QListView.Snap)
        self.listingList.setDefaultDropAction(Qt.MoveAction)
        self.listingList.setSelectionMode(QListWidget.ExtendedSelection)
        self.listingList.setStyleSheet("font-size: 14px")

        # Sale list
        self.saleList = QListWidget(self)
        self.saleList.setDragEnabled(True)
        self.saleList.setMovement(QListView.Snap)
        self.saleList.setDefaultDropAction(Qt.MoveAction)
        self.saleList.setSelectionMode(QListWidget.ExtendedSelection)
        self.saleList.setStyleSheet("font-size: 14px")

        # Context menus
        self.appraisalList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.appraisalList.customContextMenuRequested.connect(lambda event, x=ActionType.appraisal: self.OpenContextMenu(event, x))
        self.listingList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listingList.customContextMenuRequested.connect(lambda event, x=ActionType.listing: self.OpenContextMenu(event, x))
        self.saleList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.saleList.customContextMenuRequested.connect(lambda event, x=ActionType.sale: self.OpenContextMenu(event, x))

        self.layout.addWidget(self.appraisal)
        self.layout.addWidget(self.appraisalList)
        self.layout.addWidget(self.listing)
        self.layout.addWidget(self.listingList)
        self.layout.addWidget(self.sale)
        self.layout.addWidget(self.saleList)

        # Get data
        self.appraisalData = parent.parent().appraisalData
        self.listingData = parent.parent().listingData
        self.saleData = parent.parent().saleData
        self.UpdateList()

    def LoadData(self):
        if not os.path.exists(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)):
            os.makedirs(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
        try:
            with open(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + data_filename, 'r') as file:
                try:
                    jsonData = json.load(file)
                    # Default values are already set at start of class
                    self.appraisalData = jsonData.get('appraisaldata', self.appraisalData)
                    self.listingData = jsonData.get('listingdata', self.listingData)
                    self.saleData = jsonData.get('saledata', self.saleData)
                
                except json.JSONDecodeError as e:
                    print(e)

                # for data in self.appraisalData:
                #     print(self.appraisalData[data])
                # for data in self.listingData:
                #     print(self.listingData[data])
                # for data in self.saleData:
                #     print(self.saleData[data])
                
        except FileNotFoundError as e:
            print(e)

    def UpdateList(self):
        self.appraisalList.clear()
        self.listingList.clear()
        self.saleList.clear()
        for i, data in enumerate(self.appraisalData):
            self.appraisalList.insertItem(i, self.appraisalData[data]['date'] + "   " + self.appraisalData[data]['address'])
        for i, data in enumerate(self.listingData):
            self.listingList.insertItem(i, self.listingData[data]['date'] + "   " + self.listingData[data]['address'])
        for i, data in enumerate(self.saleData):
            self.saleList.insertItem(i, self.saleData[data]['date'] + "   " + self.saleData[data]['address'])

    def OpenContextMenu(self, event, actionType):
        print(actionType)
        
        menu = QMenu()

        # Actions added different depending on number of selection
        menu.addAction("Edit")
        menu.addAction("Delete")

        action = menu.exec(self.sender().mapToGlobal(event))

        if action:
            if action.text() == "Edit":
                print(self.appraisalList.selectedIndexes())
            if action.text() == "Delete":
                for item in self.appraisalList.selectedItems():
                    print("DELETE")
                    self.appraisalList.takeItem(self.appraisalList.row(item))
