from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal

class DataButton(QPushButton):
    dataChangedSignal = pyqtSignal()

    def __init__(self, default_text='', parent=None):
        super().__init__(default_text, parent)
        self._data = None
        self._defalult_text = default_text

        if default_text:
            self.setText(default_text)

    def _setID(self):
        id = str(next(iter(self._data.values()))[0])
        self.setText(id)

    def setData(self, data):
        self._data = data
        self._setID()
        self.dataChangedSignal.emit()
    
    def clear(self):
        self._data = None
        self.setText(self._defalult_text)

    def data(self):
        return self._data
