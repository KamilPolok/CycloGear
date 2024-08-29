from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QStyle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

from ..common.DataButton import DataButton
from ..common.ITrackedTab import ITrackedTab
from ..common.common_functions import create_data_input_row, create_data_display_row, create_header

from .HelpWindow import HelpWindow

class PreliminaryDataTab(ITrackedTab):
    def _view_dimensions_component(self):
        """
        Create and layout a dimensions component.
        """
        # Create header_layout
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create header
        header = create_header('Kształtowanie wału czynnego:', bold=True)

        # Create a help button
        self.help_button = QPushButton()
        help_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        self.help_button.setIcon(help_icon)
        self.help_button.setIconSize(help_icon.availableSizes()[0])  # Set the icon size to the available icon size
        self.help_button.setFixedSize(self.help_button.iconSize())  # Fit the button size to the icon size
        self.help_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Change cursor on hover
        self.help_button.setStyleSheet("border: none; background-color: transparent;")

        self.help_button.clicked.connect(self.help_window.show)

        header_layout.addWidget(header)
        header_layout.addWidget(self.help_button)

        self.main_layout.addLayout(header_layout)

        self.main_layout.addWidget(create_data_display_row(self._outputs['B'], 'B', 'Grubość koła obiegowego', decimal_precision=2))
        self.main_layout.addWidget(create_data_display_row(self._outputs['x'], 'x', 'Odległość pomiędzy kołami obiegowymi', decimal_precision=2))
        self.main_layout.addWidget(create_data_display_row(self._outputs['e'], 'e', 'Mimośród', decimal_precision=2))
        self.main_layout.addWidget(create_data_input_row(self._inputs['L'], 'L', 'Długość wału czynnego', decimal_precision=2))
        self.main_layout.addWidget(create_data_input_row(self._inputs['LA'], 'L<sub>A</sub>', 'Współrzędna podpory przesuwnej', decimal_precision=2))
        self.main_layout.addWidget(create_data_input_row(self._inputs['LB'], 'L<sub>B</sub>', 'Współrzędna podpory stałej', decimal_precision=2))
        self.main_layout.addWidget(create_data_input_row(self._inputs['L1'], 'L<sub>1</sub>', 'Współrzędna koła obiegowego nr 1', decimal_precision=2))

    def _view_eccentrics_component(self):
        self.eccentrics_layout = QVBoxLayout()

        self.main_layout.addLayout(self.eccentrics_layout)

    def update_eccentrics_component(self):
        # Loop backwards to remove and delete all items from the layout
        def clear_layout(layout):
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)

                # Remove the item from the layout
                layout.removeItem(item)

                # If the item is a widget, delete it
                if widget := item.widget():
                    widget.deleteLater()

        clear_layout(self.eccentrics_layout)
        for idx, input in enumerate(self._inputs['Lc'].values()):
            self.eccentrics_layout.addWidget(create_data_display_row(input, f'L<sub>{idx+2}</sub>', f'Współrzędne koła obiegowego nr {idx+2}', decimal_precision=2))

    def _view_material_stength_component(self):
        """
        Create and layout a material strength component.
        """
        self.main_layout.addWidget(create_header('Wytrzymałość wału czynnego:', bold=True))
        self.main_layout.addWidget(create_data_input_row(self._inputs['xz'], 'x<sub>z</sub>', 'Współczynnik bezpieczeństwa', decimal_precision=1))
        self.main_layout.addWidget(create_data_input_row(self._inputs['qdop'], 'φ\'<sub>dop</sub>', 'Dopuszczalny jednostkowy kąt skręcenia wału', decimal_precision=5))
        self.main_layout.addWidget(create_data_input_row(self._inputs['tetadop'], 'θ<sub>dop</sub>', 'Dopuszczalny kąt ugięcia wału', decimal_precision=5))
        self.main_layout.addWidget(create_data_input_row(self._inputs['fdop'], 'f<sub>dop</sub>', 'Dopuszczalna strzałka ugięcia wału', decimal_precision=5))

    def _view_material_component(self):
        """
        Create and layout a material selection component.
        """
        component_layout = QHBoxLayout()
        header = create_header('Materiał wału czynnego:', bold=True)

        self.select_material_button = DataButton('Wybierz Materiał')
        self._items['Materiał'] = self.select_material_button

        component_layout.addWidget(header)
        component_layout.addWidget(self.select_material_button)

        self.main_layout.addLayout(component_layout)
    
    def _init_help_dialog(self):
        self.help_window = HelpWindow(self)

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

        self._init_help_dialog()
        self._view_dimensions_component()
        self._view_eccentrics_component()
        self._view_material_stength_component()
        self._view_material_component()
        self.main_layout.addStretch()

        super().init_ui()
