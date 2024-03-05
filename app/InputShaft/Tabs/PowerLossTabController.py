from functools import partial

from .PowerLossTab import PowerLossTab
from ..Mediator import Mediator

from ..common.common_functions import extract_data, fetch_data_subset, update_data_subset

class PowerLossTabController:
    def __init__(self, id: int, tab: PowerLossTab, mediator: Mediator):
        self._id = id
        self._tab = tab
        self._mediator = mediator

    def _select_rolling_element(self, bearing_section_id):
        """
        Emit a signal with the updated data for the selected rolling element.

        Args:
            bearing_section_id (str): Id of section that specifies the bearing location.
        """
        self._mediator.select_rolling_element(bearing_section_id, self.get_data())
    
    def _connect_signals_and_slots(self):
        """
        Connect signals and slots for interactivity in the tab.
        """
        self._tab.allInputsProvided.connect(self._update_component_data)
        self._tab.updateStateSignal.connect(self.update_state)

        for section_name, item in self._items['Bearings'].items():
            item['rolling_elements'].clicked.connect(partial(self._select_rolling_element, section_name))
    
    def _update_component_data(self):
        self._mediator.update_component_data(self._id, self.get_data())
    
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
            data (dict): Component data.
        """
        self._component_data = component_data

        inputs_keys = [['Bearings', 'support_A', 'f'],
                       ['Bearings', 'support_B', 'f'],
                       ['Bearings', 'eccentrics', 'f']
                       ]

        outputs_keys = [['Bearings', 'support_A', 'di'], ['Bearings', 'support_A', 'do'], ['Bearings', 'support_A', 'drc'],
                        ['Bearings', 'support_B', 'di'], ['Bearings', 'support_B', 'do'], ['Bearings', 'support_B', 'drc'],
                        ['Bearings', 'eccentrics', 'di'], ['Bearings', 'eccentrics', 'do'], ['Bearings', 'eccentrics', 'drc']
                        ]

        items = [['Bearings', 'support_A', 'rolling_elements'],
                 ['Bearings', 'support_B', 'rolling_elements'],
                 ['Bearings', 'eccentrics', 'rolling_elements'],
                 ]

        self._tab_data = extract_data(self._component_data, inputs_keys+items)
        self._inputs = extract_data(self._component_data, inputs_keys)
        self._outputs = extract_data(self._component_data, outputs_keys)
        self._items = extract_data(self._component_data, items)

        self._tab.init_ui(self._items, self._inputs, self._outputs)
        self._connect_signals_and_slots()

    def update_state(self):
        """
        Update the tab with parent data.
        """
        def update_output(recipient, source, attribute):
            new_value = source[attribute][0]
            if new_value is not None:
                recipient[attribute][0].setValue(new_value)

        update_data_subset(self._component_data, self._outputs, update_output)

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

        update_data_subset(self._component_data, self._inputs, update_input)

        for name, item in self._items['Bearings'].items():
            item['rolling_elements'].setData(data['Bearings'][name]['rolling_elements'])

        self.update_state()
        self._tab.track_state(True)
