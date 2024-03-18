from .PreliminaryDataTab import PreliminaryDataTab
from .PreliminaryDataTabCalculator import PreliminaryDataTabCalculator
from ..Mediator import Mediator

from ..common.common_functions import extract_data, fetch_data_subset, update_data_subset

class PreliminaryDataTabController():
    def __init__(self, id: int, tab: PreliminaryDataTab, calculator: PreliminaryDataTabCalculator, mediator: Mediator):
        self._id = id
        self._tab = tab
        self._calculator = calculator
        self._mediator = mediator

    def _connect_signals_and_slots(self):
        """
        Connect signals and slots for interactivity in the tab.
        """
        self._tab.allInputsProvided.connect(self._update_component_data)
        self._tab.updateStateSignal.connect(self.update_state)
        
        self._tab.select_material_button.clicked.connect(self._on_select_materials)

        self._inputs['L1'][0].inputConfirmedSignal.connect(self._calculator.update_eccentrics_position)

        for name in self._validated_inputs:
            self._inputs[name][0].inputConfirmedSignal.connect(self._calculator.validate_input)

    def _update_component_data(self):
        self._mediator.update_component_data(self._id, self.get_data())

    def _on_select_materials(self):
        self._mediator.select_material()
    
    def get_data(self):
        """
        Retrieve data from the tab.

        Returns:
            self._tab_data (dict): The entered user data.
        """
        def get_input(recipient, source, attribute):
            recipient[attribute][0] = source[attribute][0].value()
        
        def get_item(recipient, source, attribute):
            recipient[attribute] = source[attribute].data()

        fetch_data_subset(self._tab_data, self._inputs, get_input)
        fetch_data_subset(self._tab_data, self._items, get_item)

        return self._tab_data
    
    def init_state(self, component_data):
        """
        Override parent method. Set the initial data for the tab from the parent's data.

        Args:
            component_data (dict): Component data.
        """
        self._component_data = component_data       

        inputs_keys = [['L'], ['LA'], ['LB'], ['L1'], ['Lc'], ['xz'], ['qdop'], ['tetadop'], ['fdop']]
        outputs_keys = [['B'], ['x']]
        items = [['Materiał']]

        self._validated_inputs = ['L', 'LA', 'LB', 'L1']

        self._tab_data = extract_data(self._component_data, inputs_keys+items)
        self._inputs = extract_data(self._component_data, inputs_keys)
        self._outputs = extract_data(self._component_data, outputs_keys)
        self._items = extract_data(self._component_data, items)
        self._calculator.init_data(self._component_data, self._inputs, self._outputs, self._validated_inputs)

        self._tab.init_ui(self._items, self._inputs, self._outputs)
        self._tab.update_eccentrics_component()
        self._connect_signals_and_slots()

    def update_state(self):
        """
        Update the tab with component data.
        """
        if len(self._tab_data['Lc']) != self._component_data['n'][0]-1:
            self._tab_data['Lc'] = extract_data(self._component_data, [['Lc']])['Lc']
            self._inputs['Lc'] = extract_data(self._component_data, [['Lc']])['Lc']
            self._tab.update_eccentrics_component()

        def update_output(recipient, source, attribute):
            new_value = source[attribute][0]
            if new_value is not None:
                recipient[attribute][0].setValue(new_value)

        update_data_subset(self._tab_data, self._outputs, update_output)

        self._calculator.update_eccentrics_position()
        self._calculator.setup_inputs_validation()

    def set_state(self, data):
        """
        Set tab's state.

        Args:
            data (dict): Data to set the state of the tab with.
        """
        self._tab.track_state(False)

        def update_input(recipient, source, attribute):
            new_value = source[attribute][0]
            if new_value is not None:
                recipient[attribute][0].setValue(new_value)

        update_data_subset(data, self._inputs, update_input)

        self._calculator.update_eccentrics_position()
        self._tab.update_selected_material(data['Materiał'])

        self.update_state()
        self._tab.track_state(True)
