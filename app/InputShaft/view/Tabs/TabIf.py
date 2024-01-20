from abc import ABCMeta, abstractmethod

from PyQt6.QtWidgets import QWidget, QLineEdit

from InputShaft.view.InputShaft import InputShaft

class ABCQWidgetMeta(ABCMeta, type(QWidget)):
    pass

class Tab(QWidget, metaclass=ABCQWidgetMeta):
    def __init__(self, parent: InputShaft, on_click_callback):
        """
        Initialize a base tab for the application.

        Args:
            parent (QWidget): The InputShaft component instance.
            on_click_callback (function): Callback function to be called on state change.
        """
        super().__init__()
        self._parent = parent
        self._on_click_callback = on_click_callback
        # Set the inputs list and dict - to track their state and verify if all inputs were provided in current tab 
        self._line_edits_states = {}
        self._items_to_select_states = {}
        # Set the dict of line edits that hold provided by user attribute values
        self.input_values = {}
        # Set the dict of (read only) line edits that hold displayed to user values 
        self.output_values = {}

        self.init_ui()
        self.setup_state_tracking()

    @abstractmethod
    def init_ui(self):
        """Initialize the user interface for the tab. Must be overridden in subclasses."""
        pass
    
    def update_tab(self):
        """Update the tab. This method can be overridden in subclasses to provide specific update logic."""
        pass

    def update_data(self):
        """Update the tab. This method can be overridden in subclasses to provide specific update logic."""
        pass
    
    def get_state(self):
        """
        Retrieve the current state of all inputs in the tab.

        Returns:
            list or None: A list of input states if all inputs are filled, otherwise None.
        """
        inputs_states = [line_edit.text() for line_edit in self._line_edits_states]
        inputs_states += [item for item in self._items_to_select_states.values()]
        return None if '' in inputs_states else inputs_states
    
    def setup_state_tracking(self):
        """
        Set up tracking for the state of input fields.
        Connects textChanged signals of QLineEdit widgets to the check_state method.
        """
        self._line_edits_states = self.findChildren(QLineEdit)
        
        for line_edit in self._line_edits_states:
            line_edit.textChanged.connect(self.check_state)

        self._original_state = self.get_state()

    def check_state(self):
        """
        Check the current state of inputs and invoke the callback function with appropriate arguments.
        This function is called whenever an input field's text is changed and on switching tab
        """
        current_state = self.get_state()
        all_filled = current_state is not None

        if all_filled:
            state_changed = current_state != self._original_state
            self._original_state = current_state
            self._on_click_callback(True, state_changed)
        else:
            self._on_click_callback(False, True)
