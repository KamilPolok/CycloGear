from PyQt6.QtWidgets import QWidget, QToolButton, QMenu, QCheckBox, QVBoxLayout, QWidgetAction
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QSize

class CheckboxDropdown(QWidget):
    stateChanged = pyqtSignal()
    def __init__(self, title="Select Options"):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.checkboxes = {}
        self.isChanged = False
        
        # Dropdown menu button
        self.dropdownButton = QToolButton(self)
        self.dropdownButton.setText(title)
        self.dropdownButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menu = QMenu(self)
        self.dropdownButton.setMenu(self.menu)

        self.dropdownButton.setIconSize(QSize(10, 10)) # Adjust the arrow size

       # Hide the default arrow and set custom styling
        self.dropdownButton.setStyleSheet("""
            QToolButton::menu-indicator {
                image: none;
            }
            QToolButton {
                font-size: 14px;
                padding-right: 10px;  /* Make room for the custom arrow */
            }
        """)
        
        self.layout.addWidget(self.dropdownButton)

    def setTitle(self, title):
        self.dropdownButton.setText(title + " \u25BC")

    def addItem(self, id, label):
        if id not in self.checkboxes:
            checkBox = QCheckBox(label, self)
            checkBox.stateChanged.connect(self._emitStateChangedSignal)
            checkWidgetAction = QWidgetAction(self)
            checkWidgetAction.setDefaultWidget(checkBox)
            self.menu.addAction(checkWidgetAction)
            self.checkboxes[id] = checkBox
    
    def enableItem(self, id, enabled=True):
        if id in self.checkboxes:
            self.checkboxes[id].setEnabled(enabled)
        if enabled is False:
             self.checkboxes[id].setChecked(enabled)

    def currentOptions(self):
        res = []
        for id, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                res.append((id, checkbox.text()))
        return res

    def _emitStateChangedSignal(self):
        self.stateChanged.emit()
