"""Details tab"""

import uuid

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMenu, QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QDate, pyqtSlot, QVariant

from constants import uuid_namespace, ActionType, SortType

from customsubclasses import CustomQListWidget
from detailspopup import DetailEdit, DetailConvert

class DetailsWidget(QWidget):
    propertyData = {}
    sortType = SortType.date
    sortOrder = Qt.DescendingOrder

    dialog = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dataParent = parent.parent()
        self.layout = QVBoxLayout(self)

        # Sorting options setup
        self.bLayout = QHBoxLayout()
        self.sortLabel = QLabel("Sort by:", self)
        self.sortTypeButton = QPushButton("Date", self)
        self.sortOrderButton = QPushButton("Descending", self)
        self.sortLabel.setFixedWidth(60)
        self.sortTypeButton.clicked.connect(self.ChangeSortType)
        self.sortOrderButton.clicked.connect(self.ChangeSortOrder)
        self.bLayout.addWidget(self.sortLabel)
        self.bLayout.addWidget(self.sortTypeButton)
        self.bLayout.addWidget(self.sortOrderButton)

        # Label setup
        self.appraisal = QLabel("Appraisals")
        self.appraisal.setStyleSheet("font-size: 18px")
        self.listing = QLabel("Listings")
        self.listing.setStyleSheet("font-size: 18px")
        self.sale = QLabel("Sales")
        self.sale.setStyleSheet("font-size: 18px")

        # List setup
        self.appraisalList = CustomQListWidget(self)
        self.listingList = CustomQListWidget(self)
        self.saleList = CustomQListWidget(self)
        
        # self.appraisalList.setEditTriggers(QListWidget.DoubleClicked)
        self.appraisalList.setSortingEnabled(True)
        self.listingList.setSortingEnabled(True)
        self.saleList.setSortingEnabled(True)
        self.appraisalList.sortItems(self.sortOrder)
        self.listingList.sortItems(self.sortOrder)
        self.saleList.sortItems(self.sortOrder)

        # Context menus
        self.appraisalList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.appraisalList.customContextMenuRequested.connect(lambda event, x=ActionType.appraisal: self.OpenContextMenu(event, x))
        self.listingList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listingList.customContextMenuRequested.connect(lambda event, x=ActionType.listing: self.OpenContextMenu(event, x))
        self.saleList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.saleList.customContextMenuRequested.connect(lambda event, x=ActionType.sale: self.OpenContextMenu(event, x))

        self.layout.addLayout(self.bLayout)
        self.layout.addWidget(self.appraisal)
        self.layout.addWidget(self.appraisalList)
        self.layout.addWidget(self.listing)
        self.layout.addWidget(self.listingList)
        self.layout.addWidget(self.sale)
        self.layout.addWidget(self.saleList)

    def UpdateList(self):
        self.appraisalList.clear()
        self.listingList.clear()
        self.saleList.clear()
        for data in self.dataParent.propertyData:
            if 'appraisal_date' in self.dataParent.propertyData[data]:
                widgetText = self.AddressToString(data, ActionType.appraisal)
                
                item = QListWidgetItem(widgetText, self.appraisalList)
                item.setData(Qt.UserRole, self.dataParent.propertyData[data])
                item.setData(Qt.UserRole + 1, data)
                self.appraisalList.addItem(item)
            if 'listing_date' in self.dataParent.propertyData[data]:
                widgetText = self.AddressToString(data, ActionType.listing)
                
                item = QListWidgetItem(widgetText, self.listingList)
                item.setData(Qt.UserRole, self.dataParent.propertyData[data])
                item.setData(Qt.UserRole + 1, data)
                self.listingList.addItem(item)
            if 'sale_date' in self.dataParent.propertyData[data]:
                widgetText = self.AddressToString(data, ActionType.sale)
                
                item = QListWidgetItem(
                    widgetText + "\t $" +
                    f"{self.dataParent.propertyData[data]['price']:,.0f}" + " @ " +
                    f"{self.dataParent.propertyData[data]['commission']:,.2f}" + "%",
                    self.saleList
                )
                item.setData(Qt.UserRole, self.dataParent.propertyData[data])
                item.setData(Qt.UserRole + 1, data)
                self.saleList.addItem(item)

    @pyqtSlot(ActionType, QVariant, dict, QDate)
    @pyqtSlot(ActionType, QVariant, dict, QDate, int, float)
    def UpdateDetails(self, actionType, a_uuid, address, date, price=0, commission=0):
        date = date.toString('yyyy/MM/dd')
        data = self.dataParent.propertyData[a_uuid]
        data |= address

        if actionType is ActionType.appraisal:
            data |= {'appraisal_date': date}
        elif actionType is ActionType.listing:
            data |= {'listing_date': date}
        elif actionType is ActionType.sale:
            data |= {'sale_date': date, 'price': price, 'commission': commission}
        
        self.dataParent.propertyData |= {a_uuid: data}
        self.UpdateList()

    def DeleteDetails(self, actionType, a_uuid):
        if actionType is ActionType.appraisal:
            self.dataParent.propertyData[a_uuid].pop('appraisal_date', None)
        elif actionType is ActionType.listing:
            self.dataParent.propertyData[a_uuid].pop('listing_date', None)
        elif actionType is ActionType.sale:
            self.dataParent.propertyData[a_uuid].pop('sale_date', None)
            self.dataParent.propertyData[a_uuid].pop('price', None)
            self.dataParent.propertyData[a_uuid].pop('commission', None)

    @pyqtSlot(ActionType, QVariant, QDate)
    @pyqtSlot(ActionType, QVariant, QDate, int, float)
    def ConvertDetails(self, actionType, a_uuid, date, price=0, commission=0):
        date = date.toString('yyyy/MM/dd')
        data = self.dataParent.propertyData[a_uuid]
        
        if actionType is ActionType.appraisal:
            data |= {'listing_date': date}
        elif actionType is ActionType.listing:
            data |= {'sale_date': date, 'price': price, 'commission': commission}
        
        self.dataParent.propertyData |= {a_uuid: data}
        self.UpdateList()

    def OpenContextMenu(self, event, actionType):
        # If nothing selected, don't open a menu
        if len(self.appraisalList.selectedItems()) + len(self.listingList.selectedItems()) + len(self.saleList.selectedItems()) == 0:
            return
        # Otherwise
        menu = QMenu()
        menu.addAction("Edit")
        menu.addAction("Delete")

        # Actions added different depending on number of selection
        if actionType is ActionType.appraisal:
            menu.addSeparator()
            menu.addAction("Convert to listing")
        elif actionType is ActionType.listing:
            menu.addSeparator()
            menu.addAction("Convert to sale")

        # Get menu data (and open at click position)
        action = menu.exec(self.sender().mapToGlobal(event))
        if not action:
            return

        # After all checks have passed
        # Handle appraisal case
        if actionType is ActionType.appraisal:
            if action.text() == "Edit":
                self.dialog = DetailEdit(
                    actionType,
                    self.appraisalList.currentItem().data(Qt.UserRole + 1),
                    self.appraisalList.currentItem().data(Qt.UserRole)['address'],
                    QDate.fromString(self.appraisalList.currentItem().data(Qt.UserRole)['appraisal_date'], 'yyyy/MM/dd'),
                    parent=self.parent().parent()
                )
                self.dialog.okPressed[ActionType, QVariant, dict, QDate].connect(self.UpdateDetails)

            elif action.text() == "Delete":
                # Get information about the item to be deleted
                item = self.appraisalList.takeItem(self.appraisalList.currentRow())
                # Delete entry from data dictionary
                self.DeleteDetails(ActionType.appraisal, item.data(Qt.UserRole)['address'])

            elif action.text() == "Convert to listing":
                self.dialog = DetailConvert(
                    actionType,
                    self.appraisalList.currentItem().data(Qt.UserRole + 1),
                    self.appraisalList.currentItem().data(Qt.UserRole)['address'],
                    QDate.fromString(self.appraisalList.currentItem().data(Qt.UserRole)['appraisal_date'], 'yyyy/MM/dd'),
                    parent=self.parent().parent()
                )
                self.dialog.okPressed[ActionType, QVariant, QDate].connect(self.ConvertDetails)

        # Handle listing case
        elif actionType is ActionType.listing:
            if action.text() == "Edit":
                self.dialog = DetailEdit(
                    actionType,
                    self.listingList.currentItem().data(Qt.UserRole + 1),
                    self.listingList.currentItem().data(Qt.UserRole)['address'],
                    QDate.fromString(self.listingList.currentItem().data(Qt.UserRole)['listing_date'], 'yyyy/MM/dd'),
                    parent=self.parent().parent()
                )
                self.dialog.okPressed[ActionType, QVariant, dict, QDate].connect(self.UpdateDetails)

            elif action.text() == "Delete":
                # Get information about the item to be deleted
                item = self.listingList.takeItem(self.listingList.currentRow())
                # Delete entry from data dictionary
                self.DeleteDetails(ActionType.listing, item.data(Qt.UserRole)['address'])

            elif action.text() == "Convert to sale":
                self.dialog = DetailConvert(
                    actionType,
                    self.listingList.currentItem().data(Qt.UserRole + 1),
                    self.listingList.currentItem().data(Qt.UserRole)['address'],
                    QDate.fromString(self.listingList.currentItem().data(Qt.UserRole)['listing_date'], 'yyyy/MM/dd'),
                    parent=self.parent().parent()
                )
                self.dialog.okPressed[ActionType, QVariant, QDate, int, float].connect(self.ConvertDetails)

        # Handle sale case
        elif actionType is ActionType.sale:
            if action.text() == "Edit":
                self.dialog = DetailEdit(
                    actionType,
                    self.saleList.currentItem().data(Qt.UserRole + 1),
                    self.saleList.currentItem().data(Qt.UserRole)['address'],
                    QDate.fromString(self.saleList.currentItem().data(Qt.UserRole)['sale_date'], 'yyyy/MM/dd'),
                    self.saleList.currentItem().data(Qt.UserRole)['price'],
                    self.saleList.currentItem().data(Qt.UserRole)['commission'],
                    parent=self.parent().parent()
                )
                self.dialog.okPressed[ActionType, QVariant, dict, QDate, int, float].connect(self.UpdateDetails)

            elif action.text() == "Delete":
                # Get information about the item to be deleted
                item = self.saleList.takeItem(self.saleList.currentRow())
                # Delete entry from data dictionary
                self.DeleteDetails(ActionType.sale, item.data(Qt.UserRole)['address'])

    def ChangeSortType(self):
        if self.sortType is SortType.date:
            self.sortType = SortType.suburb
            self.sortTypeButton.setText("Suburb")
        elif self.sortType is SortType.suburb:
            self.sortType = SortType.street
            self.sortTypeButton.setText("Street")
        elif self.sortType is SortType.street:
            self.sortType = SortType.number
            self.sortTypeButton.setText("Number")
        elif self.sortType is SortType.number:
            self.sortType = SortType.date
            self.sortTypeButton.setText("Date")
        self.UpdateList()

    def ChangeSortOrder(self):
        if self.sortOrder is Qt.DescendingOrder:
            self.sortOrder = Qt.AscendingOrder
            self.sortOrderButton.setText("Ascending")
        elif self.sortOrder is Qt.AscendingOrder:
            self.sortOrder = Qt.DescendingOrder
            self.sortOrderButton.setText("Descending")
            
        self.appraisalList.sortItems(self.sortOrder)
        self.listingList.sortItems(self.sortOrder)
        self.saleList.sortItems(self.sortOrder)
        self.UpdateList()

    def AddressToString(self, data, actionType):
        if actionType is ActionType.appraisal:
            date = self.dataParent.propertyData[data]['appraisal_date']
        if actionType is ActionType.listing:
            date = self.dataParent.propertyData[data]['listing_date']
        if actionType is ActionType.sale:
            date = self.dataParent.propertyData[data]['sale_date']

        if self.sortType is SortType.date:
            return (
                date + "\t " +
                self.dataParent.propertyData[data]['address']['number'] + " " +
                self.dataParent.propertyData[data]['address']['street'] + ", " +
                self.dataParent.propertyData[data]['address']['suburb'] + " " +
                self.dataParent.propertyData[data]['address']['postcode']
            )
        elif self.sortType is SortType.suburb:
            return (
                self.dataParent.propertyData[data]['address']['suburb'] + " " +
                self.dataParent.propertyData[data]['address']['postcode'] + ", " +
                self.dataParent.propertyData[data]['address']['street'] + ", " +
                self.dataParent.propertyData[data]['address']['number'] + "\t " +
                date
            )
        elif self.sortType is SortType.street:
            return (
                self.dataParent.propertyData[data]['address']['street'] + ", " +
                self.dataParent.propertyData[data]['address']['number'] + ", " +
                self.dataParent.propertyData[data]['address']['suburb'] + " " +
                self.dataParent.propertyData[data]['address']['postcode'] + "\t " +
                date
            )
        elif self.sortType is SortType.number:
            return (
                self.dataParent.propertyData[data]['address']['number'] + " " +
                self.dataParent.propertyData[data]['address']['street'] + ", " +
                self.dataParent.propertyData[data]['address']['suburb'] + " " +
                self.dataParent.propertyData[data]['address']['postcode'] + "\t " +
                date
            )
