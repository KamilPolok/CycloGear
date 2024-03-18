from abc import ABCMeta, abstractmethod

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QWidget

from .Input import Input
from .Output import Output

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

    def _connect_signals_and_slots(self):
        """
        Connect signals from every tracket input, output and item
        to method that checks the state.
        """
        for input in self._inputs_to_provide:
            input.inputConfirmedSignal.connect(self._check_state)

        for output in self._outputs_to_provide:
            output.textChanged.connect(self._check_state)

        for item in self._items_to_select:
            item.dataChangedSignal.connect(self._check_state)
    
    def _disconnect_signals_and_slots(self):
        """
        Disconnect signals from every tracket input, output and item
        from method that checks the state.

        If the objects does not exist or their signals are not connected,
        do nothing, else disconnect the signals.
        """
        try:
            for input in self._inputs_to_provide:
                input.inputConfirmedSignal.disconnect(self._check_state)

            for output in self._outputs_to_provide:
                output.textChanged.disconnect(self._check_state)

            for item in self._items_to_select:
                item.dataChangedSignal.disconnect(self._check_state)
        except (TypeError, AttributeError):
            pass

    def _setup_state_tracking(self):
        """
        Set up inputs tracking.

        Connect inputConfirmedSignal and dataChangedSignal signals of custom Input and DataButton 
        widgets to the _check_state method.
        """
        self._disconnect_signals_and_slots()

        self._inputs_to_provide = self.findChildren(Input)
        self._outputs_to_provide = self.findChildren(Output)
        self._items_to_select = self.findChildren(DataButton)

        self._connect_signals_and_slots()

        self._original_state = self._get_state()

    def _get_state(self):
        """
        Retrieve the current state of all inputs in the widget.

        Returns:
            list : A list of values that the tracked inputs, outputs and items ale holding.
        """
        inputs_states = [input.value() for input in self._inputs_to_provide]
        inputs_states += [output.value() for output in self._outputs_to_provide]
        inputs_states += [item.id() for item in self._items_to_select]

        return inputs_states

    def _check_state(self):
        """
        Check the current state of subjects and invoke the callback function with appropriate arguments.

        This function is called whenever an input is changed. It checks the state of inputs in the
        widget, and calls the callback function.
        """
        all_provided, state_changed = self.check_status()

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

    def check_status(self):
        """
        Check status of all tracked subjects.

        Returns:
            all_provided (bool): Are all inputs provided?
            state_changed (bool): Were the inputs changed?
        """
        state_changed = False
        current_state = self._get_state()

        # Check if all inputs were provided
        all_provided = all(current_state)

        state_changed = current_state != self._original_state

        self._original_state = current_state
        return all_provided, state_changed
    
    def track_state(self, track):
        if track:
            self._disconnect_signals_and_slots()
            self._connect_signals_and_slots()
            self._original_state = self._get_state()
        else:
            self._disconnect_signals_and_slots()
        
        tracked_children = self.findChildren(ITrackedWidget)
        for tracked_child in tracked_children:
            tracked_child.track_state(track)

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
