from abc import ABCMeta, abstractmethod

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QWidget

from .Input import Input
from .DataButton import DataButton

class ABCQWidgetMeta(ABCMeta, type(QWidget)):
    pass

class ITrackedWidget(QWidget, metaclass=ABCQWidgetMeta):
    """
    Widget that tracks its status.

    It provides a reusable interface for checking if all the inputs are provided and/or changed.
    """
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self._parent = parent

        if callback:
            self._callback = callback
    
    def _setup_state_tracking(self):
        """
        Set up inputs tracking.

        Connect inputConfirmedSignal and dataChangedSignal signals of custom Input and DataButton 
        widgets to the _check_state method.
        """
        self._inputs_to_provide = self.findChildren(Input)

        for input in self._inputs_to_provide:
            input.inputConfirmedSignal.connect(self._check_state)

        self._items_to_select = self.findChildren(DataButton)

        for item in self._items_to_select:
            item.dataChangedSignal.connect(self._check_state)

        self._original_state = self._get_state()

    def _get_state(self):
        """
        Retrieve the current state of all inputs in the widget.

        Returns:
            list or None: A list of input states if all inputs are filled, otherwise None.
        """
        inputs_states = [input.value() for input in self._inputs_to_provide]
        inputs_states += [item.id() for item in self._items_to_select]

        return inputs_states

    def _check_state(self):
        """
        Check the current state of inputs and invoke the callback function with appropriate arguments.

        This function is called whenever an input is changed. It checks the state of inputs in the
        widget, and calls the callback function.
        """
        state_changed = False
        current_state = self._get_state()

        # Check if all inputs were provided
        all_provided = all(current_state)

        # Check if current state changed from no inputs provided to all inputs provided
        # It is for ignoring the state change after setting the widget initial state
        if not (all(input is None for input in self._original_state) and all_provided):
            state_changed = current_state != self._original_state

        self._original_state = current_state

        self._on_state_checked(all_provided, state_changed)

    def _on_state_checked(self, all_provided, state_changed):
        """
        Perform tasks after state checking.

        Call the callback function with widget status attributes.

        Args:
            all_provided (bool): Are all inputs provided?
            state_changed (bool): Were the inputs changed?
        """
        self._callback(all_provided, state_changed)

    def _on_activated(self):
        """
        Call appropriate methods time when the widget becomes visible.
        """
        self._check_state()
    
    def showEvent(self, event):
        """
        Override the showEvent method of the QWidget to implement custom logic
        (call _on_tab_activated() method) to execute when the widget becomes visible.

        Args:
            event: (QEvent)
        """
        if event.type() == QEvent.Type.Show:
            self._on_activated()
        super().showEvent(event)
    
    def set_callback(self, callback):
        """
        Set callback

        Args:
            callback (callable): Function that should be called after state checking.
        """
        self._callback = callback
    
    @abstractmethod
    def init_ui(self):
        """
        Initialize the user interface for the widget. Must be overridden in subclasses.
        """
        self._setup_state_tracking()
