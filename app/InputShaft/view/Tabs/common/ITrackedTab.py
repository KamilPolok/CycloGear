from .ITrackedWidget import ITrackedWidget

class ITrackedTab(ITrackedWidget):
    """
    Tab widget that extends the ITrackedWidget abstract class:
    - implement methods that should be overriden (but do not have to) by subclasses
    - override parent class method to implement additional functionalities
    """
    def __init__(self, parent, callback):
        # Set the dict of inputs that hold provided by user attribute values
        self.input_values = {}
        # Set the dict of outputs that hold presented to user values
        self.output_values = {}
        super().__init__(parent, callback)

    def update_tab(self):
        """
        Update the tab data. This method can be overridden in subclasses to provide specific update logic.
        """
        pass

    def update_data(self):
        """
        Update the data. This method can be overridden in subclasses to provide specific update logic.
        """
        pass

    def _on_state_checked(self, all_filled, state_changed):
        """
        Override parent class method to perform additional tasks after state checking.

        Update the data.
        """
        if all_filled:
            self.update_data()

        super()._on_state_checked(all_filled, state_changed)
    
    def _on_activated(self):
        """
        Override parent class method to call additional methods uppon activation.
        """
        super()._on_activated()

        self.update_tab()
