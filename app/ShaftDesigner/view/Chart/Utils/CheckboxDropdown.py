from PyQt6.QtWidgets import QToolButton, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import pyqtSignal

class StayOpenMenu(QMenu):
    def mouseReleaseEvent(self, event):
        action = self.activeAction()
        if action and action.isCheckable():
            action.trigger()
            return
        super().mouseReleaseEvent(event)

class CheckboxDropdown(QToolButton):
    """
    A custom QToolButton that displays a dropdown menu with checkboxes.
    """
    stateChanged = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.actions = {}

        self.setStyleSheet("""
            * { padding-right: 3px }
            QToolButton::menu-indicator { image: none }                                
        """)

        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self._menu = StayOpenMenu(self)
        self._menu.setToolTipsVisible(True)
        self.setMenu(self._menu)

    def addItem(self, id, label, description='', callback=None):
        """
        Add a checkable action to the dropdown menu.
        """
        if id not in self.actions:
            action = QAction(label, self)
            action.setCheckable(True)
            action.setToolTip(description)
            if callback is None:
                action.triggered.connect(self._emitStateChangedSignal)
            else:
                action.triggered.connect(callback)
            self._menu.addAction(action)
            self.actions[id] = action
    
    def enableItem(self, id, enable=True):
        '''
        Enables or disables checkbox of given id.
        If disables, unchecks it.

        Args:
            id (str): id of checkbox.
            enabled (bool): if enable checkbox.
        '''
        if id in self.actions:
            self.actions[id].setEnabled(enable)
        if enable is False:
            self.actions[id].setChecked(enable)
            self._emitStateChangedSignal()

    def checkItem(self, id, check):
        if id in self.actions:
            if check != self.isChecked(id):
                self.actions[id].trigger()

    def isChecked(self, id):
        '''
        Check if Checkbox is checked.

        Args:
            id: (str): id of checkbox.

        Returns:
            res (bool): If checkobox of given id is checked.
        '''
        if id in self.actions:
            return self.actions[id].isChecked()
        return False
    
    def setIcon(self, icon, tootltip):
        '''
        Set icon of every checkbox.
        '''
        super().setIcon(QIcon(icon))

        self.setToolTip(tootltip)

    def getItems(self):
        """
        Return all items ids. 
        Returns:
            res (list): List of tuples (id, text) for of every checked checkbox.
        """
        res = []
        for id in self.actions.keys():
                res.append(id)
        return res

    def getCheckedItems(self):
        """
        Return checked items ids.

        Returns:
            res (list): List of tuples (id, text) for of every checked checkbox.
        """
        res = []
        for id, action in self.actions.items():
            if action.isChecked():
                res.append(id)
        return res

    def _emitStateChangedSignal(self):
        self.stateChanged.emit()
