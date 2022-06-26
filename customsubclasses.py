"""GUI"""

from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QToolButton, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from constants import SortType
import re

class CustomToolButton(QToolButton):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.setIconSize(QSize(40, 40))
        self.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

class CustomQListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        # self.setMovement(QListView.Snap)
        # self.setDefaultDropAction(Qt.MoveAction)
        # self.setDragDropMode(QListWidget.InternalMove)
        self.setSelectionMode(QListWidget.SingleSelection)
        # self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setStyleSheet("font-size: 14px")
    

    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.selectionModel().clear()
        super(CustomQListWidget, self).mousePressEvent(event)
    
    # Focus handler
    def focusInEvent(self, _):
        self._parent.WidgetFocusManager(self)

class CustomQListWidgetItem(QListWidgetItem):
    # Add variables
    sortType = SortType.date

    def __lt__(self, other):
        # Use custom sorting based on the data given in qt.userrole
        try:
            if(self.sortType is SortType.date):
                return self.data(Qt.UserRole + 2) < other.data(Qt.UserRole + 2)
            elif(self.sortType is SortType.number):
                st = self.data(Qt.UserRole)['address']['number']
                ot = other.data(Qt.UserRole)['address']['number']
                st = int(re.findall(r'\d+', st)[-1])
                ot = int(re.findall(r'\d+', ot)[-1])
                return st < ot
            elif(self.sortType is SortType.street):
                return self.data(Qt.UserRole)['address']['street'].lower() < other.data(Qt.UserRole)['address']['street'].lower()
            elif(self.sortType is SortType.suburb):
                return self.data(Qt.UserRole)['address']['suburb'].lower() < other.data(Qt.UserRole)['address']['suburb'].lower()
            
            # Other scenarios
            return QListWidgetItem.__lt__(self,other)
        except:
            return QListWidgetItem.__lt__(self,other)

class StretchedLabel(QLabel):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))