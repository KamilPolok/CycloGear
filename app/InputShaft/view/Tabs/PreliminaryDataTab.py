from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from .TabIf import Tab
from .TabCommon import create_data_input_row

class PreliminaryDataTab(Tab):
    updated_data_signal = pyqtSignal(dict)

    def _set_tab_data(self):
        """
        Initialize tab data from the parent's data.
        """
        attributes_to_acquire = ['L', 'LA', 'LB', 'L1', 'Materiał', 'xz', 'qdop', 'tetadop', 'fdop']
        self.tab_data = {attr: self._parent.data[attr] for attr in attributes_to_acquire}
        self._items_to_select_states['Materiał'] = ''

    def init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._set_tab_data()

        self.setLayout(QVBoxLayout())

        self._view_dimensions_component()
        self._view_material_stength_component()
        self._view_material_component()

    def _view_dimensions_component(self):
        """
        Create and layout the dimensions component of the tab.
        """
        component_layout = QVBoxLayout()
        component_label = QLabel('Wymiary:')

        shaft_length = create_data_input_row(self, 'L', 'Długość wału wejściowego', 'L')
        roller_support = create_data_input_row(self, 'LA', 'Współrzędne podpory przesuwnej', 'L<sub>A</sub>')
        pin_support = create_data_input_row(self, 'LB', 'Współrzędne podpory nieprzesuwnej', 'L<sub>B</sub>')
        cyclo_disc1 = create_data_input_row(self, 'L1', 'Współrzędne koła obiegowego 1', 'L<sub>1</sub>')

        component_layout.addWidget(component_label)
        component_layout.addLayout(shaft_length)
        component_layout.addLayout(roller_support)
        component_layout.addLayout(pin_support)
        component_layout.addLayout(cyclo_disc1)

        self.layout().addLayout(component_layout)

    def _view_material_stength_component(self):
        """
        Create and layout the  component of the tab.
        """
        component_layout = QVBoxLayout()
        component_label = QLabel('Pozostałe:')

        factor_of_safety = create_data_input_row(self, 'xz', 'Współczynnik bezpieczeństwa', 'x<sub>z</sub>')
        permissible_angle_of_twist = create_data_input_row(self, 'qdop', 'Dopuszczalny jednostkowy kąt skręcenia wału', 'φ\'<sub>dop</sub>')
        permissible_deflecton_angle = create_data_input_row(self, 'tetadop', 'Dopuszczalna kąt ugięcia', 'θ<sub>dop</sub>')
        permissible_deflection_arrow = create_data_input_row(self, 'fdop', 'Dopuszczalna strzałka ugięcia', 'f<sub>dop</sub>')

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

        self.select_material_button = QPushButton('Wybierz Materiał')

        component_layout.addWidget(component_label)
        component_layout.addWidget(self.select_material_button)

        self.layout().addLayout(component_layout)

    def update_viewed_material(self, item_data):
        """
        Update the displayed material information.

        :param item_data: Dictionary containing material data.
        """
        self.select_material_button.setText(str(item_data['Oznaczenie'][0]))
        self.tab_data['Materiał'] = item_data

        self._items_to_select_states['Materiał'] = str(item_data['Oznaczenie'][0])
        self.check_state()

    def get_data(self):
        """
        Retrieve data from the input fields.

        :return: Dictionary of the tab's data.
        """
        for attribute, line_edit in self.input_values.items():
            text = line_edit.text()
            value = literal_eval(text)
            self.tab_data[attribute][0] = value

        return self.tab_data

    def update_data(self):
        """
        Emit a signal to update the tab's data.
        """
        tab_data = self.get_data()
        self.updated_data_signal.emit(tab_data)
