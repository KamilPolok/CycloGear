from abc import ABCMeta, abstractmethod

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QWidget

from .Input import Input

class ABCQWidgetMeta(ABCMeta, type(QWidget)):
    pass

class ITrackedWidget(QWidget, metaclass=ABCQWidgetMeta):
    """
    Widget which inputs - line edits, items that have to be selected by the
    user are tracked.

    It provides a reusable interface for checking if all the inputs are provided
    and/or changed.
    """
    def __init__(self, parent, callback):
        super().__init__(parent)
        self._parent = parent
        self._callback = callback

        self._items_to_select = {}

        self._init_ui()
        self._setup_state_tracking()

    @abstractmethod
    def _init_ui(self):
        """Initialize the user interface for the widget. Must be overridden in subclasses."""
        pass
    
    def _setup_state_tracking(self):
        """
        Set up inputs tracking.

        Connects textChanged signals of QLineEdit widgets to the _check_state method,
        and provides a dictionary where subclasses can add other inputs that should be tracked.
        """
        self._inputs_to_provide = self.findChildren(Input)

        for input in self._inputs_to_provide:
            input.inputConfirmedSignal.connect(self._check_state)

        self._original_state = self._get_state()

    def _get_state(self):
        """
        Retrieve the current state of all inputs in the widget.

        Returns:
            list or None: A list of input states if all inputs are filled, otherwise None.
        """
        inputs_states = [input.text() for input in self._inputs_to_provide]
        inputs_states += [item for item in self._items_to_select.values()]
        return None if '' in inputs_states else inputs_states

    def _check_state(self):
        """
        Check the current state of inputs and invoke the callback function with appropriate arguments.

        This function is called whenever an input is changed. It checks the state of inputs in the
        widget, and calls the callback function.
        """
        current_state = self._get_state()

        all_filled = current_state is not None
        state_changed = current_state != self._original_state

        if all_filled:
            self._original_state = current_state
        
        self._callback(all_filled, state_changed)
    
    def showEvent(self, event):
        """
        Override the showEvent method of the QWidget to implement custom logic
        (call _on_tab_activated() method) to execute when the widget is shown.

        param: event
        """
        if event.type() == QEvent.Type.Show:
            self._on_activated()
        super().showEvent(event)
    
    def _on_activated(self):
        """
        This method is triggered every time when widget becomes visible and calls appropriate methods.
        """
        self._check_state()
