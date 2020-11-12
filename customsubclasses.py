"""GUI"""

from PyQt5.QtWidgets import QLabel, QListWidget, QToolButton, QSizePolicy
from PyQt5.QtCore import Qt, QSize

class CustomToolButton(QToolButton):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.setIconSize(QSize(40, 40))
        self.setToolButtonStyle(Qt.ToolButtonStyle(Qt.ToolButtonTextUnderIcon))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

class CustomQListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # self.setMovement(QListView.Snap)
        # self.setDefaultDropAction(Qt.MoveAction)
        # self.setDragDropMode(QListWidget.InternalMove)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setStyleSheet("font-size: 14px")

class StretchedLabel(QLabel):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
