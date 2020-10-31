"""GUI"""

from PyQt5.QtWidgets import QLabel, QSizePolicy

class StretchedLabel(QLabel):
    def __init__(self, *args, **kargs):
        super(StretchedLabel, self).__init__(*args, **kargs)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))  

        self.setStyleSheet("font-size: 26px;")
