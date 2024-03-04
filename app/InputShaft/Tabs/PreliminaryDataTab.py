from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from .common.DataButton import DataButton
from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_input_row, create_data_display_row

class PreliminaryDataTab(ITrackedTab):
    def _view_dimensions_component(self):
        """
        Create and layout a dimensions component.
        """
        component_layout = QVBoxLayout()

        component_layout.addWidget(QLabel('Wymiary:'))
        component_layout.addLayout(create_data_input_row(self, self._inputs['L'], 'L', 'Długość wału wejściowego', decimal_precision=2))
        component_layout.addLayout(create_data_input_row(self, self._inputs['LA'], 'L<sub>A</sub>', 'Współrzędne podpory przesuwnej', decimal_precision=2))
        component_layout.addLayout(create_data_input_row(self, self._inputs['LB'], 'L<sub>B</sub>', 'Współrzędne podpory nieprzesuwnej', decimal_precision=2))
        component_layout.addLayout(create_data_input_row(self, self._inputs['L1'], 'L<sub>1</sub>', 'Współrzędne koła obiegowego 1', decimal_precision=2))
        component_layout.addLayout(create_data_display_row(self, self._outputs['L2'], 'L<sub>2</sub>', 'Współrzędne koła obiegowego 2', decimal_precision=2))
        component_layout.addLayout(create_data_display_row(self, self._outputs['x'], 'x', 'Odległość pomiędzy tarczami', decimal_precision=2))
        component_layout.addLayout(create_data_display_row(self, self._outputs['B'], 'B', 'Grubość tarczy', decimal_precision=2))

        self.main_layout.addLayout(component_layout)

    def _view_material_stength_component(self):
        """
        Create and layout a material strength component.
        """
        component_layout = QVBoxLayout()

        component_layout.addWidget(QLabel('Pozostałe:'))
        component_layout.addLayout(create_data_input_row(self, self._inputs['xz'], 'x<sub>z</sub>', 'Współczynnik bezpieczeństwa', decimal_precision=1))
        component_layout.addLayout(create_data_input_row(self, self._inputs['qdop'], 'φ\'<sub>dop</sub>', 'Dopuszczalny jednostkowy kąt skręcenia wału', decimal_precision=5))
        component_layout.addLayout(create_data_input_row(self, self._inputs['tetadop'], 'θ<sub>dop</sub>', 'Dopuszczalny kąt ugięcia', decimal_precision=5))
        component_layout.addLayout(create_data_input_row(self, self._inputs['fdop'], 'f<sub>dop</sub>', 'Dopuszczalna strzałka ugięcia', decimal_precision=5))
        self.main_layout.addLayout(component_layout)

    def _view_material_component(self):
        """
        Create and layout a material selection component.
        """
        component_layout = QHBoxLayout()
        component_label = QLabel('Materiał:')

        self.select_material_button = DataButton('Wybierz Materiał')
        self._items['Materiał'] = self.select_material_button

        component_layout.addWidget(component_label)
        component_layout.addWidget(self.select_material_button)

        self.main_layout.addLayout(component_layout)

    def update_selected_material(self, item_data):
        """
        Update the displayed material information.

        Args:
            item_data (dict): Material data.
        """
        self.select_material_button.setData(item_data)

    def init_ui(self, items, inputs, outputs):
        """
        Initialize the user interface for this tab.

        Args:
            items: (dict): DattaButtons providing storage for selected items
            inputs (dict): Inputs
            outputs (dict): Outputs
        """
        self._items = items
        self._inputs = inputs
        self._outputs = outputs

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self._view_dimensions_component()
        self._view_material_stength_component()
        self._view_material_component()

        super().init_ui()
