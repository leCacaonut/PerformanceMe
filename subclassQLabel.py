"""GUI"""

from PyQt5.QtWidgets import QLabel, QSizePolicy

class StretchedLabel(QLabel):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
