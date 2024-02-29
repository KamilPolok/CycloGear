from copy import deepcopy

from .PreliminaryDataTab import PreliminaryDataTab
from .PreliminaryDataTabCalculator import PreliminaryDataTabCalculator
from ..Mediator import Mediator

class PreliminaryDataTabController():
    def __init__(self, id: int, tab: PreliminaryDataTab, calculator: PreliminaryDataTabCalculator, mediator: Mediator):
        self._id = id
        self._tab = tab
        self._calculator = calculator
        self._mediator = mediator

        self._inputs = {}
        self._outputs = {}
        self._items = {}

    def _connect_signals_and_slots(self):
        """
        Connect signals and slots for interactivity in the tab.
        """
        self._tab.allInputsProvided.connect(self._update_component_data)
        self._tab.updateStateSignal.connect(self.update_state)
        
        self._tab.select_material_button.clicked.connect(self._on_select_materials)

        self._inputs['L1'].inputConfirmedSignal.connect(self._calculator.update_eccentrics_position)

        for name in self.validated_inputs:
            self._inputs[name].inputConfirmedSignal.connect(self._calculator.validate_input)

    def _update_component_data(self):
        tab_data = self.get_data()
        self._mediator.update_component_data(self._id, tab_data)

    def _on_select_materials(self):
        self._mediator.select_material()
    
    def get_data(self):
        """
        Retrieve data from the tab.

        Returns:
            (dict): The formatted data from the tab.
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

        attributes_to_acquire = ['L', 'LA', 'LB', 'L1', 'L2', 'Materiał', 'xz', 'qdop', 'tetadop', 'fdop']
        self.tab_data = {attr: deepcopy(self._component_data[attr]) for attr in attributes_to_acquire}

        self.validated_inputs = ['L', 'LA', 'LB', 'L1']
        self._calculator.init_data(self._component_data, self._inputs, self._outputs, self.validated_inputs)
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

        self._calculator.update_eccentrics_position()
        self._calculator.setup_inputs_validation()

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

        self._calculator.update_eccentrics_position()

        self._tab.update_selected_material(data['Materiał'])
