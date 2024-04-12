from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QWidget

from .common.DataButton import DataButton
from .common.Section import Section
from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_display_row, create_data_input_row

class PowerLossTab(ITrackedTab):
    def _init_selector(self):
        self.layout_selector = QComboBox()
        self.layout_selector.addItems(["Podpora przesuwna A", "Podpora stała B", "Wykorbienia"])
        self.layout_selector.currentIndexChanged.connect(self._change_section)
        self.main_layout.addWidget(self.layout_selector)

    def _init_sections(self):
        containers = self._init_bearings_sections()
        
        self.stacked_sections = QStackedWidget()
        for container in containers:
            self.stacked_sections.addWidget(container)

        self.main_layout.addWidget(self.stacked_sections)

    def _init_bearings_sections(self):
        """
        Create and layout the UI components for bearings sections.
        """
        containers = []
        for section_name in self._items['Bearings']:
            section_layout = QVBoxLayout()

            # Set content container
            container = QWidget()
            container.setLayout(section_layout)

            # Set section for displaying outputs and inputs
            section = Section(self, section_name, self._enable_select_rolling_element_button)

            # Set data display and input rows
            section.addLayout(create_data_input_row(self, self._inputs['Bearings'][section_name]['f'], 'f', 'Współczynnik tarcia tocznego łożyska', decimal_precision=2))
            section.addLayout(create_data_display_row(self, self._outputs['Bearings'][section_name]['di'], 'd', 'Średnica wewnętrzna łożyska', decimal_precision=2))
            section.addLayout(create_data_display_row(self, self._outputs['Bearings'][section_name]['do'], 'D', 'Średnica zewnętrzna łożyska', decimal_precision=2))
            section.addLayout(create_data_display_row(self, self._outputs['Bearings'][section_name]['drc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))

            # Set button for bearing selection
            button_layout = QHBoxLayout()
            button_label = QLabel('Element toczny o znormalizowanej średnicy:')

            select_rolling_element_button = DataButton('Wybierz element toczny')
            self._items['Bearings'][section_name]['rolling_elements'] = select_rolling_element_button

            button_layout.addWidget(button_label)
            button_layout.addWidget(select_rolling_element_button)

            section_layout.addWidget(section)
            section_layout.addLayout(button_layout)

            containers.append(container)

        return containers
    
    def _change_section(self, index):
        self.stacked_sections.setCurrentIndex(index)
    
    def _enable_select_rolling_element_button(self, section_name, enable_button, delete_choice):
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
