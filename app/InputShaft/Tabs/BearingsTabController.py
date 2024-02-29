from copy import deepcopy

from .BearingsTab import BearingsTab
from ..Mediator import Mediator

class BearingsTabController:
    def __init__(self, id: int, tab: BearingsTab, mediator: Mediator):
        self._id = id
        self._tab = tab
        self._mediator = mediator

        self._inputs = {}
        self._outputs = {}
        self._items = {}

    def _select_support_A_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self._mediator.select_support_A_bearing(tab_data)

    def _select_support_B_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self._mediator.select_support_B_bearing(tab_data)

    def _select_central_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self._mediator.select_central_bearing(tab_data)
    
    def _connect_signals_and_slots(self):
        """
        Connect signals and slots for interactivity in the tab.
        """
        self._tab.allInputsProvided.connect(self._update_component_data)
        self._tab.updateStateSignal.connect(self.update_state)

        self._tab._select_support_A_bearing_button.clicked.connect(self._select_support_A_bearing)
        self._tab._select_support_B_bearing_button.clicked.connect(self._select_support_B_bearing)
        self._tab._select_central_bearing_button.clicked.connect(self._select_central_bearing)

    def _update_component_data(self):
        tab_data = self.get_data()
        self._mediator.update_component_data(self._id, tab_data)
    
    def get_data(self):
        """
        Retrieve data from the tab.

        Returns:
            dict: The formatted data from the tab.
        """
        for attribute, input in self._inputs.items():
            self.tab_data[attribute][0] = input.value()

        for attribute, item in self._items.items():
            self.tab_data[attribute] = item.data()

        return self.tab_data
    
    def init_state(self, component_data):
        """
        Override parent method. Set the initial data for the tab from the parent's data.

        Args:
            component_data (dict): Component data.
        """
        self._component_data = component_data
        
        attributes_to_acquire = ['LhA', 'fdA', 'ftA',
                                 'LhB', 'fdB', 'ftB', 
                                 'Lhc', 'fdc', 'ftc']
        self.tab_data = {attr: deepcopy(self._component_data[attr]) for attr in attributes_to_acquire}
        self._tab.init_ui(self._component_data, self.tab_data, self._items, self._inputs, self._outputs)
        self._connect_signals_and_slots()

    def update_state(self):
        """
        Update the tab with component data.
        """
        for attribute in self._outputs.keys():
            new_value = self._component_data[attribute][0]
            if new_value is not None:
                self._outputs[attribute].setValue(new_value)
    
    def set_state(self, data):
        """
        Set tab's state.

        Args:
            data (dict): Data to set the state of the tab with.
        """
        for attribute, input in self._inputs.items():
            value = data[attribute][0]
            if value is not None:
                input.setValue(value)

        self._tab.update_selected_support_A_bearing(data['Łożyska_podpora_A'])
        self._tab.update_selected_support_B_bearing(data['Łożyska_podpora_B'])
        self._tab.update_selected_central_bearing(data['Łożyska_centralne'])
