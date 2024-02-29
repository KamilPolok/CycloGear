from PyQt6.QtCore import pyqtSignal

from .ITrackedWidget import ITrackedWidget

class ITrackedTab(ITrackedWidget):
    """
    Tab widget that extends the ITrackedWidget abstract class:
    - implement methods that should be overriden (but do not have to) by subclasses
    - override parent class method to implement additional functionalities
    """
    updateStateSignal = pyqtSignal()
    allInputsProvided = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

    def _on_state_checked(self, all_filled, state_changed):
        """
        Override parent class method to perform additional tasks after state checking.

        Update the data.
        """
        if all_filled:
            self.allInputsProvided.emit()

        super()._on_state_checked(all_filled, state_changed)
    
    def _on_activated(self):
        """
        Override parent class method to call additional methods uppon activation.
        """
        super()._on_activated()

        self.updateStateSignal.emit()
