from copy import deepcopy

from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from .common.DataButton import DataButton
from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_input_row, create_data_display_row

class PreliminaryDataTab(ITrackedTab):
    update_data_signal = pyqtSignal(dict)

    def _set_tab_data(self):
        """
        Initialize tab data from the parent's data.
        """
        attributes_to_acquire = ['L', 'LA', 'LB', 'L1', 'L2', 'Materiał', 'xz', 'qdop', 'tetadop', 'fdop']
        self.tab_data = {attr: deepcopy(self._parent.data[attr]) for attr in attributes_to_acquire}
        self._items = {}

    def _init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._set_tab_data()

        self.setLayout(QVBoxLayout())

        self._view_dimensions_component()
        self._view_material_stength_component()
        self._view_material_component()

        self._connect_signals_and_slots()

    def _view_dimensions_component(self):
        """
        Create and layout the dimensions component of the tab.
        """
        component_layout = QVBoxLayout()
        component_label = QLabel('Wymiary:')

        shaft_length = create_data_input_row(self, 'L', 'Długość wału wejściowego', 'L', decimal_precision=2)
        roller_support = create_data_input_row(self, 'LA', 'Współrzędne podpory przesuwnej', 'L<sub>A</sub>', decimal_precision=2)
        pin_support = create_data_input_row(self, 'LB', 'Współrzędne podpory nieprzesuwnej', 'L<sub>B</sub>', decimal_precision=2)
        cyclo_disc1 = create_data_input_row(self, 'L1', 'Współrzędne koła obiegowego 1', 'L<sub>1</sub>', decimal_precision=2)
        cyclo_disc2 = create_data_display_row(self, 'L2', self._parent.data['L2'], 'L<sub>2</sub>', 'Współrzędne koła obiegowego 2', decimal_precision=2)
        disc_width = create_data_display_row(self, 'x', self._parent.data['x'], 'x', 'Odległość pomiędzy tarczami', decimal_precision=2)
        discs_distance = create_data_display_row(self, 'B', self._parent.data['B'], 'B', 'Grubość tarczy', decimal_precision=2)

        component_layout.addWidget(component_label)
        component_layout.addLayout(shaft_length)
        component_layout.addLayout(roller_support)
        component_layout.addLayout(pin_support)
        component_layout.addLayout(cyclo_disc1)
        component_layout.addLayout(cyclo_disc2)
        component_layout.addLayout(disc_width)
        component_layout.addLayout(discs_distance)

        self.layout().addLayout(component_layout)

    def _view_material_stength_component(self):
        """
        Create and layout the  component of the tab.
        """
        component_layout = QVBoxLayout()
        component_label = QLabel('Pozostałe:')

        factor_of_safety = create_data_input_row(self, 'xz', 'Współczynnik bezpieczeństwa', 'x<sub>z</sub>', decimal_precision=1)
        permissible_angle_of_twist = create_data_input_row(self, 'qdop', 'Dopuszczalny jednostkowy kąt skręcenia wału', 'φ\'<sub>dop</sub>', decimal_precision=5)
        permissible_deflecton_angle = create_data_input_row(self, 'tetadop', 'Dopuszczalna kąt ugięcia', 'θ<sub>dop</sub>', decimal_precision=5)
        permissible_deflection_arrow = create_data_input_row(self, 'fdop', 'Dopuszczalna strzałka ugięcia', 'f<sub>dop</sub>', decimal_precision=5)

        component_layout.addWidget(component_label)
        component_layout.addLayout(factor_of_safety)
        component_layout.addLayout(permissible_angle_of_twist)
        component_layout.addLayout(permissible_deflecton_angle)
        component_layout.addLayout(permissible_deflection_arrow)


        self.layout().addLayout(component_layout)

    def _view_material_component(self):
        """
        Create and layout the third co mponent of the tab.
        """
        component_layout = QHBoxLayout()
        component_label = QLabel('Materiał:')

        self.select_material_button = DataButton('Wybierz Materiał')
        self._items['Materiał'] = self.select_material_button

        component_layout.addWidget(component_label)
        component_layout.addWidget(self.select_material_button)

        self.layout().addLayout(component_layout)

    def _connect_signals_and_slots(self):
        """
        Connect signals and slots for interactivity in the tab
        """
        self._inputs['L1'].inputConfirmedSignal.connect(self._update_eccentrics_position)

        self.validated_inputs = ['L', 'LA', 'LB', 'L1']
        for name in self.validated_inputs:
            self._inputs[name].inputConfirmedSignal.connect(self._validate_input)

    def _update_eccentrics_position(self):
        """
        This function gets triggered when the user changes the position
        of the first eccentric. It calculates and updates the positions
        of the following eccentrics.
        """
        value = self._inputs['L1'].value()
        if value:
            L1 = value
            x = self._parent.data['x'][0]
            B = self._parent.data['B'][0]
            L2 = L1 + x + B
            self._outputs['L2'].setValue(L2)
        else:
            self._outputs['L2'].clear()
    
    def _setup_inputs_validation(self):
        """
        This function gets triggered when the user switches onto current ITrackedTab.
        It (re)initializes and applies the input limits of the validated_inputs.
        """
        self.validated_inputs_limits = {}
        self.validated_inputs_values = {}

        self._set_input_limits('L')
        for name in self.validated_inputs:
            if self._inputs[name].isEnabled():
                self._validate_input(self._inputs[name])

    def _validate_input(self, input=None):
        """
        This function gets triggered when the user confirms the given input or at the limits 
        (re)initialization. It checks if the input is valid and depending on the result, takes actions.

        :param input: input which content is validated
        """
        input = self.sender() if input == None else input
        input_name = next((name for name, i in self._inputs.items() if i == input), None)
        if self._is_input_valid(input_name):
            self._enable_next_input(input_name)
        else:
            self._inputs[input_name].clear()
            self._clear_and_disable_subsequent_inputs(input_name)
    
    def _is_input_valid(self, input_name):
        """
        This function gets triggered when the user confirms the given input or at the limits 
        (re)initialization. It checks if the input is valid and depending on the result, takes actions.

        :param input: input which content is validated
        :return: Boolean value representing the validity of teh input
        """
        input = self._inputs[input_name]
        value = input.value()
        if value is None:
            return False
        
        min_value, max_value = self.validated_inputs_limits[input_name]
        if min_value <= value <= max_value:
            self.validated_inputs_values[input_name] = value
            return True
        return False
    
    def _enable_next_input(self, input_name):
        """
        Enable the next input from validated inputs after the one which name is provided and if its value 
        is invalid clears its text.

        :param input: name of input before the input to enable
        """
        idx = self.validated_inputs.index(input_name)
        if idx < len(self.validated_inputs) - 1:
            next_input_name = self.validated_inputs[idx + 1]
            self._inputs[next_input_name].setEnabled(True)
            self._set_input_limits(next_input_name)
            if not self._is_input_valid(next_input_name):
                self._inputs[next_input_name].clear()
    
    def _clear_and_disable_subsequent_inputs(self, input_name):
        """
        Clear text from and disable all the validated inputs that come after the input which name is 
        provided.

        :param input: name of the input after which perform the the disabling
        """
        idx = self.validated_inputs.index(input_name)
        for name in self.validated_inputs[idx + 1:]:
            self._inputs[name].setPlaceholderText('')
            self._inputs[name].clear()
            self._inputs[name].setDisabled(True)
        self._outputs['L2'].clear()

    def _set_input_limits(self, input_name):
        """
        Calculate, set and save the limits for the input which name was provided.

        :param input: name of the input for which the limits are set
        """

        if input_name == 'L':
            min_value = self._parent.data['x'][0] + 2 * self._parent.data['B'][0]
            max_value = 1000
        elif input_name == 'LA':
            min_value = 0
            max_value = self.validated_inputs_values['L']
        elif input_name == 'LB':
            min_value = self.validated_inputs_values['LA'] + 2 * self._parent.data['B'][0] + self._parent.data['x'][0]
            max_value = self.validated_inputs_values['L']
        elif input_name == 'L1':
            min_value =  self.validated_inputs_values['LA'] + 0.5 * self._parent.data['B'][0]
            max_value = self.validated_inputs_values['LB'] - self._parent.data['x'][0] - 1.5 * self._parent.data['B'][0]
        
        self.validated_inputs_limits[input_name] = (round(min_value, 2), round(max_value, 2))
        self._inputs[input_name].setPlaceholderText(f"{min_value:.2f}-{max_value:.2f}")

    def _on_activated(self):
        """
        Override parents method to call additional methods when this tab becomes active.
        """
        super()._on_activated()
        
        self._update_eccentrics_position()
        self._setup_inputs_validation()

    def update_selected_material(self, item_data):
        """
        Update the displayed material information.

        :param item_data: Dictionary containing material data.
        """
        self.select_material_button.setData(item_data)

    def get_data(self):
        """
        Retrieve data from the input fields.

        :return: Dictionary of the tab's data.
        """
        for attribute, input in self._inputs.items():
            self.tab_data[attribute][0] = input.value()

        for attribute, item in self._items.items():
            self.tab_data[attribute] = item.data()

        return self.tab_data
    
    def set_tab(self, data):
        for attribute, line_edit in self._inputs.items():
            value = data[attribute][0]
            if value is not None:
                line_edit.setValue(value)

        self._update_eccentrics_position()

        self.select_material_button.setData(data['Materiał'])

    def update_data(self):
        """
        Emit a signal to update the tab's data.
        """
        tab_data = self.get_data()
        self.update_data_signal.emit(tab_data)
