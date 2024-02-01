
from PyQt6.QtCore import pyqtSignal, QObject

class Mediator(QObject):
    shaftDesigningFinished = pyqtSignal()

    def emit_shaft_designing_finished(self):
        self.shaftDesigningFinished.emit()