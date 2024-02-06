from PyQt6.QtCore import QEvent

from .ITrackedWidget import ITrackedWidget

class ITrackedTab(ITrackedWidget):
    """
    Tab that extends the ITrackedWidget abstract class with methods that should be overriden 
    (but do not have to) by subclasses 
    """
    def __init__(self, parent, callback):
        # Set the dict of inputs that hold provided by user attribute values
        self.input_values = {}
        # Set the dict of outputs that hold presented to user values
        self.output_values = {}
        super().__init__(parent, callback)

    def update_tab(self):
        """Update the tab data. This method can be overridden in subclasses to provide specific update logic."""
        pass

    def update_data(self):
        """Update the data. This method can be overridden in subclasses to provide specific update logic."""
        pass
    
    def showEvent(self, event):
        """
        Override the showEvent method of the QWidget to implement custom logic
        (call _on_tab_activated() method) to execute when the tab is shown.

        param: event
        """
        if event.type() == QEvent.Type.Show:
            self._on_tab_activated()
        super().showEvent(event)
    
    def _on_tab_activated(self):
        """
        This method is triggered every time when the tab becomes active and calls appropriate methods.
        """
        self._check_state()

        self.update_tab()

    def _check_state(self):
        """
        Overloads the parent class method - execute the the update_data method
        when all the inputs are filled.
        """
        current_state = self._get_state()

        all_filled = current_state is not None
        state_changed = current_state != self._original_state

        if all_filled:
            self.update_data()
            self._original_state = current_state
        
        self._callback(all_filled, state_changed)
