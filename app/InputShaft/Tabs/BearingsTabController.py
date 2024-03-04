from .BearingsTab import BearingsTab
from ..Mediator import Mediator

from ..common.common_functions import extract_data, fetch_data_subset, update_data_subset

class BearingsTabController:
    def __init__(self, id: int, tab: BearingsTab, mediator: Mediator):
        self._id = id
        self._tab = tab
        self._mediator = mediator

    def _select_support_A_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        self._mediator.select_support_A_bearing(self.get_data())

    def _select_support_B_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        self._mediator.select_support_B_bearing(self.get_data())

    def _select_central_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        self._mediator.select_central_bearing(self.get_data())
    
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
        Override parent method. Set the initial data for the tab from the component's data.

        Args:
            component_data (dict): Component data.
        """
        self._component_data = component_data

        inputs_keys = [['Bearings', 'support_A', 'Lh'], ['Bearings', 'support_A', 'fd'], ['Bearings', 'support_A', 'ft'],
                       ['Bearings', 'support_B', 'Lh'], ['Bearings', 'support_B', 'fd'], ['Bearings', 'support_B', 'ft'],
                       ['Bearings', 'eccentrics', 'Lh'], ['Bearings', 'eccentrics', 'fd'], ['Bearings', 'eccentrics', 'ft']
                       ]
                    
        outputs_keys = [['Bearings', 'support_A', 'dip'],
                        ['Bearings', 'support_B', 'dip'],
                        ['Bearings', 'eccentrics', 'dip']
                        ]
        
        items = [['Bearings', 'support_A', 'data'],
                 ['Bearings', 'support_B', 'data'],
                 ['Bearings', 'eccentrics', 'data'],
                 ]
        
        self._tab_data = extract_data(self._component_data, inputs_keys+items)
        self._inputs = extract_data(self._component_data, inputs_keys)
        self._outputs = extract_data(self._component_data, outputs_keys)
        self._items = extract_data(self._component_data, items)

        self._tab.init_ui(self._items, self._inputs, self._outputs)
        self._connect_signals_and_slots()

    def update_state(self):
        """
        Update the tab with component data.
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
        def update_input(recipient, source, attribute):
            new_value = source[attribute][0]
            if new_value is not None:
                recipient[attribute][0].setValue(new_value)
        
        update_data_subset(self._component_data, self._inputs, update_input)

        self._tab.update_selected_support_A_bearing(data['Bearings']['support_A']['data'])
        self._tab.update_selected_support_B_bearing(data['Bearings']['support_B']['data'])
        self._tab.update_selected_central_bearing(data['Bearings']['eccentrics']['data'])
