from typing import Callable
from PyQt6.QtWidgets import QLayout, QVBoxLayout, QWidget

from .ITrackedWidget import ITrackedWidget

class Section(ITrackedWidget):
    """
    QWidget instance that derrives from ITrackedWidget abstract class.

    It implements a basic widget like class.
    """
    def __init__(self, parent: QWidget, name: str, callback: Callable):
        """
        parent (QWidget): Parent (UI) of this module.
        name (str): instance ID.
        callback (Callable): method to be called 
        """
        super().__init__(parent, callback)
        self.init_ui()

        self._name = name

    def init_ui(self):
        """
        Init the user interface.
        """
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

    def addWidget(self, widget: QWidget):
        """
        Add widget.

        Args:
            widget (QWidget): widget to add.
        """
        self.main_layout.addWidget(widget)
        self._setup_state_tracking()

    def addLayout(self, layout: QLayout):
        """
        Add layout.

        Args:
            layout (QWidget): layout to add.
        """
        self.main_layout.addLayout(layout)
        self._setup_state_tracking()

    def _on_state_checked(self, all_provided: bool, state_changed: bool):
        """
        Override the parent class method called after state checking.

        Add name to the callback attributes.

        Args:
            all_provided (bool): Speciefies whether all inputs are provided.
            state_changed (bool): Speciefies whether the inputs has been changed.
        """
        self._callback(self._name, all_provided, state_changed)
