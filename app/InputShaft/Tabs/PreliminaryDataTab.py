from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from .common.DataButton import DataButton
from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_input_row, create_data_display_row

class PreliminaryDataTab(ITrackedTab):
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
        cyclo_disc2 = create_data_display_row(self, 'L2', self._component_data['L2'], 'L<sub>2</sub>', 'Współrzędne koła obiegowego 2', decimal_precision=2)
        disc_width = create_data_display_row(self, 'x', self._component_data['x'], 'x', 'Odległość pomiędzy tarczami', decimal_precision=2)
        discs_distance = create_data_display_row(self, 'B', self._component_data['B'], 'B', 'Grubość tarczy', decimal_precision=2)

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

    def update_selected_material(self, item_data):
        """
        Update the displayed material information.

        Args:
            item_data (dict): Material data.
        """
        self.select_material_button.setData(item_data)

    def init_ui(self, component_data, tab_data, items, inputs, outputs):
        """
        Initialize the user interface for this tab.
        """
        self._component_data = component_data

        self.tab_data = tab_data
        self._items = items

        self._inputs = inputs
        self._outputs = outputs

        self.setLayout(QVBoxLayout())

        self._view_dimensions_component()
        self._view_material_stength_component()
        self._view_material_component()

        super().init_ui()
