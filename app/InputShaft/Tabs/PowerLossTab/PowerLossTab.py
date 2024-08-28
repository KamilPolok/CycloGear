from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget

from ..common.DataButton import DataButton
from ..common.Section import Section
from ..common.ITrackedTab import ITrackedTab
from ..common.common_functions import create_data_display_row, create_data_input_row, create_header

class PowerLossTab(ITrackedTab):
    rollingElementDiameterProvided = pyqtSignal(str, bool, bool)
    sectionDataProvided = pyqtSignal(str, bool, bool)

    def _init_selector(self):
        selector_layout = QHBoxLayout()

        layout_selector_label = create_header('Miejsce osadzenia łożyska:', bold=True)

        self.layout_selector = QComboBox()
        self.layout_selector.setFixedWidth(150)
        self.layout_selector.setEditable(True)
        line_edit = self.layout_selector.lineEdit()
        line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_edit.setReadOnly(True)
        
        self.layout_selector.addItems(["Podpora przesuwna A", "Podpora stała B", "Mimośrody"])
        self.layout_selector.currentIndexChanged.connect(self._on_change_section)

        selector_layout.addWidget(layout_selector_label, alignment=Qt.AlignmentFlag.AlignLeft)
        selector_layout.addWidget(self.layout_selector, alignment=Qt.AlignmentFlag.AlignLeft)
        selector_layout.addStretch(1)

        self.main_layout.addLayout(selector_layout)

    def _init_sections(self):
        self.stacked_sections = QStackedWidget()

        for section_name in self._items['Bearings']:
            container = self._init_bearings_section(section_name)
            self.stacked_sections.addWidget(container)

        self.main_layout.addWidget(self.stacked_sections)

    def _init_bearings_section(self, section_name):
        """
        Create and layout the UI components for single bearing section.
        """
        section_layout = QVBoxLayout()

        # Set content container
        container = QWidget()
        container.setLayout(section_layout)

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = create_header('Element toczny o znormalizowanej średnicy:', bold=True)

        select_rolling_element_button = DataButton('Wybierz element toczny')
        self._items['Bearings'][section_name]['rolling_elements'] = select_rolling_element_button
        button_layout.addWidget(button_label)
        button_layout.addWidget(select_rolling_element_button)

        # Set bearing diameter subsection
        diameter_subsection = Section(self, section_name, self.rollingElementDiameterProvided.emit)
        diameter_subsection.addWidget(create_data_display_row(self._outputs['Bearings'][section_name]['di'], 'd', 'Średnica wewnętrzna łożyska', decimal_precision=2))
        diameter_subsection.addWidget(create_data_display_row(self._outputs['Bearings'][section_name]['do'], 'D', 'Średnica zewnętrzna łożyska', decimal_precision=2))
        diameter_subsection.addWidget(create_data_display_row(self._outputs['Bearings'][section_name]['drc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))

        # Set data subsection
        data_subsection = Section(self, section_name, self.sectionDataProvided.emit)
        data_subsection.addLayout(button_layout)
        data_subsection.addWidget(create_data_input_row(self._inputs['Bearings'][section_name]['f'], 'f', 'Współczynnik tarcia tocznego łożyska', decimal_precision=5))

        # Add widgets to section layout
        section_layout.addWidget(diameter_subsection)
        section_layout.addWidget(data_subsection)
        section_layout.addWidget(create_data_display_row(self._inputs['Bearings'][section_name]['P'], 'P', 'Straty mocy', decimal_precision=2))

        return container
    
    def _on_change_section(self, index):
        """
        Perform actions on section change.
        """
        self.stacked_sections.setCurrentIndex(index)

        # Call method on_activated for every subsection in activated section
        [section.on_activated() for section in self.stacked_sections.currentWidget().findChildren(Section)]
    
    def enable_select_rolling_element_button(self, section_name, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.

        Args:
            section_name (str): Specifies the bearing location.
            enable_button (bool): Specifies whether the button should be enabled or disabled.
            delete_choice (bool): Specifies whether the button should be reseted (clearing its id and data).
        """
        self._items['Bearings'][section_name]['rolling_elements'].setEnabled(enable_button)

        if delete_choice:
            self._items['Bearings'][section_name]['rolling_elements'].clear()
    
    def update_selected_rolling_element(self, section_name, item_data):
        """
        Update selected rolling element.

        Args:
            section_name (str): Specifies the bearing location.
            item_data (dict): Data of the selected item.
        """
        self._items['Bearings'][section_name]['rolling_elements'].setData(item_data)
    
    def init_ui(self, items, inputs, outputs):
        """
        Initialize the user interface for this tab.
        
        Args:
            items (dict): DattaButtons providing storage for selected items.
            inputs (dict): Inputs.
            outputs (dict): Outputs.
        """
        self._items = items
        self._inputs = inputs
        self._outputs = outputs

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self._init_selector()
        self._init_sections()
        super().init_ui()
