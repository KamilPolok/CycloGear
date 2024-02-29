from .ResultsTab import ResultsTab

class ResultsTabController:
    def __init__(self, id: int, tab: ResultsTab, mediator):
        self._id = id
        self._tab = tab
        self._mediator = mediator

        self._inputs = {}
        self._outputs = {}
        self._items = {}

    def _connect_signals_and_slots(self):
        self._tab.updateStateSignal.connect(self.update_state)


    def init_state(self, component_data):
        """
        Override parent method. Set the initial data for the tab from the parent's data.

        Args:
            component_data (dict): Component data.
        """
        self._component_data = component_data
        
        self._tab.init_ui(self._component_data, self._outputs)
        self._connect_signals_and_slots()
    
    def update_state(self):
        """
        Update the tab with parent data.
        """
        for attribute in self._outputs.keys():
            new_value = self._component_data[attribute][0]
            self._outputs[attribute].setValue(new_value)
