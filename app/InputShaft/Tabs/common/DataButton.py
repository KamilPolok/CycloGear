from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal

class DataButton(QPushButton):
    dataChangedSignal = pyqtSignal(object)

    def __init__(self, default_text='', parent=None):
        super().__init__(default_text, parent)
        self._data = None
        self._id = None
        self._defalult_text = default_text

        if default_text:
            self.setText(default_text)

    def _setID(self):
        self._id = str(next(iter(self._data.values()))[0])
        self.setText(self._id)

    def setData(self, data):
        if data:
            self._data = data
            self._setID()
            self.dataChangedSignal.emit(self._data)
    
    def clear(self):
        self._data = None
        self._id = None
        self.setText(self._defalult_text)
        self.dataChangedSignal.emit(self._data)

    def id(self):
        return self._id

    def data(self):
        return self._data
