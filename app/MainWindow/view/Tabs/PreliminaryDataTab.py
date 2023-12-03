from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from .TabIf import Tab
from .TabCommon import create_data_input_row

class PreliminaryDataTab(Tab):
    updated_data_signal = pyqtSignal(dict)

    def _set_tab_data(self):
        """
        Initialize tab data from the main window's data.
        """
        attributes_to_acquire = ['L', 'L1', 'L2', 'LA', 'LB', 'Materiał', 'xz']
        self.tab_data = {attr: self._window.data[attr] for attr in attributes_to_acquire}
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

        support_coordinates_label = QLabel('Współrzędne podpór:')
        pin_support = create_data_input_row(self, 'LA', 'Podpora stała A', 'L<sub>A</sub>')
        roller_support = create_data_input_row(self, 'LB', 'Podpora przesuwna B', 'L<sub>B</sub>')

        cyclo_disc_coordinates_label = QLabel('Współrzędne tarcz obiegowych:')
        cyclo_disc1 = create_data_input_row(self, 'L1', 'Tarcza obiegowa 1', 'L<sub>1</sub>')
        cyclo_disc2 = create_data_input_row(self, 'L2', 'Tarcza obiegowa 2', 'L<sub>2</sub>')

        component_layout.addWidget(component_label)
        component_layout.addLayout(shaft_length)
        component_layout.addWidget(support_coordinates_label)
        component_layout.addLayout(pin_support)
        component_layout.addLayout(roller_support)
        component_layout.addWidget(cyclo_disc_coordinates_label)
        component_layout.addLayout(cyclo_disc1)
        component_layout.addLayout(cyclo_disc2)

        self.layout().addLayout(component_layout)

    def _view_material_stength_component(self):
        """
        Create and layout the  component of the tab.
        """
        component_layout = QVBoxLayout()
        component_label = QLabel('Współczynnik bezpieczeństwa:')

        factor_of_safety = create_data_input_row(self, 'xz', '', 'x<sub>z</sub>')

        component_layout.addWidget(component_label)
        component_layout.addLayout(factor_of_safety)

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
