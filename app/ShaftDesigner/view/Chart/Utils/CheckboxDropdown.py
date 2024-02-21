from PyQt6.QtWidgets import QToolButton, QMenu, QCheckBox, QWidgetAction
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QSize

class CheckboxDropdown(QToolButton):
    """
    A custom QToolButton that displays a dropdown menu with checkboxes.
    """
    stateChanged = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.checkboxes = {}
        self.isChanged = False

        self.setStyleSheet("""
            * { padding-right: 3px }
            QToolButton::menu-indicator { image: none }                                
            QToolButton {
                background-color: transparent;
                color: white;
                border: 2px solid transparent;
                border-radius: 5px;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #c1c9c9;
                border: 1px solid #a9b0b0;
            }
            QToolButton:pressed {
                background-color: #c1c9c9;
                border: 1px solid #a9b0b0;
            }
        """)
        self.setIconSize(QSize(20, 20))
        self.setFixedSize(QSize(35, 35))

        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self._menu = QMenu(self)
        self.setMenu(self._menu)

    def addItem(self, id, label, callback=None):
        """
        Add a checkbox item to the dropdown menu.
        """
        if id not in self.checkboxes:
            checkBox = QCheckBox(label, self)
            checkWidgetAction = QWidgetAction(self)
            checkWidgetAction.setDefaultWidget(checkBox)
            self._menu.addAction(checkWidgetAction)
            self.checkboxes[id] = checkBox
            if callback == None:
                checkBox.stateChanged.connect(self._emitStateChangedSignal)
            else:
                checkBox.stateChanged.connect(callback)
    
    def enableItem(self, id, enabled=True):
        '''
        Enables or disables checkbox of given id.
        If disables, unchecks it.

        Args:
            id (str): id of checkbox.
            enabled (bool): if enable checkbox.
        '''
        if id in self.checkboxes:
            self.checkboxes[id].setEnabled(enabled)
        if enabled is False:
             self.checkboxes[id].setChecked(enabled)

    def isChecked(self, id):
        '''
        Check if Checkbox is checked.

        Args:
            id: (str): id of checkbox.

        Returns:
            res (bool): If checkobox of given id is checked.
        '''
        if id in self.checkboxes:
            checkbox = self.checkboxes[id]
            return checkbox.isChecked()
        return False
    
    def setIcon(self, icon, tootltip):
        '''
        Set icon of every checkbox.
        '''
        super().setIcon(QIcon(icon))

        self.setToolTip(tootltip)

    def currentOptions(self):
        """
        Return checkboxes that are currently checked

        Returns:
            res (list): List of tuples (id, text) for of every checked checkbox.
        """
        res = []
        for id, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                res.append((id, checkbox.text()))
        return res

    def _emitStateChangedSignal(self):
        self.stateChanged.emit()
