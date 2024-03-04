from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QWidget

from .common.DataButton import DataButton
from .common.ITrackedWidget import ITrackedWidget
from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_display_row, create_data_input_row

class Section(ITrackedWidget):
    def __init__(self, parent, callback):
        super().__init__(parent, callback)

        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def addLayout(self, layout):
        self.main_layout.addLayout(layout)
        self._setup_state_tracking()

    def insertLayout(self, idx, layout):
        self.main_layout.insertLayout(idx, layout)

class PowerLossTab(ITrackedTab):
    def _init_selector(self):
        self.layout_selector = QComboBox()
        self.layout_selector.addItems(["Podpora przesuwna A", "Podpora przesuwna B", "Wykorbienia"])
        self.layout_selector.currentIndexChanged.connect(self._change_section)
        self.main_layout.addWidget(self.layout_selector)

    def _init_sections(self):
        self._init_support_A_bearing_section()
        self._init_support_B_bearing_section()
        self._init_central_bearing_section()

        self.stacked_sections = QStackedWidget()
        self.stacked_sections.addWidget(self.section_A)
        self.stacked_sections.addWidget(self.section_B)
        self.stacked_sections.addWidget(self.section_central)

        self.main_layout.addWidget(self.stacked_sections)

    def _init_support_A_bearing_section(self):
        """
        Create and layout the UI components for the support A bearing section.
        """
        section_layout = QVBoxLayout()

        self.section_A = QWidget()
        self.section_A.setLayout(section_layout)

        # Set content container
        self.support_A_bearing_section = Section(self, self._enable_select_support_A_bearing_rolling_element_button)

        # Set data display and input rows
        self.support_A_bearing_section.addLayout(create_data_input_row(self, self._inputs['Bearings']['support_A']['f'], 'f', 'Współczynnik tarcia tocznego', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_A']['di'], 'd', 'Średnica wewnętrzna łożyska', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_A']['do'], 'D', 'Średnica zewnętrzna łożyska', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_A']['drc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))
        
        # Set button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')

        self._select_support_A_bearing_rolling_element_button = DataButton('Wybierz elementy toczne')
        self._items['Bearings']['support_A']['rolling_elements'] = self._select_support_A_bearing_rolling_element_button

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_A_bearing_rolling_element_button)

        section_layout.addWidget(self.support_A_bearing_section)
        section_layout.addLayout(button_layout)

    def _init_support_B_bearing_section(self):
        """
        Create and layout the UI components for the support B bearing section.
        """
        section_layout = QVBoxLayout()

        self.section_B = QWidget()
        self.section_B.setLayout(section_layout)

        self.support_B_bearing_section = Section(self, self._enable_select_support_B_bearing_rolling_element_button)

        # Set data display and input rows
        self.support_B_bearing_section.addLayout(create_data_input_row(self, self._inputs['Bearings']['support_B']['f'], 'f', 'Współczynnik tarcia tocznego', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_B']['di'], 'd', 'Średnica wewnętrzna łożyska', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_B']['do'], 'D', 'Średnica zewnętrzna łożyska', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['support_B']['drc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))
        
        # Set button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')

        self._select_support_B_bearing_rolling_element_button = DataButton('Wybierz elementy toczne')
        self._items['Bearings']['support_B']['rolling_elements'] = self._select_support_B_bearing_rolling_element_button

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_B_bearing_rolling_element_button)

        section_layout.addWidget(self.support_B_bearing_section)
        section_layout.addLayout(button_layout)

    def _init_central_bearing_section(self):
        """
        Create and layout the UI components for the central bearing section.
        """
        section_layout = QVBoxLayout()

        self.section_central = QWidget()
        self.section_central.setLayout(section_layout)

        self.central_bearing_section = Section(self, self._enable_select_central_bearing_rolling_element_button)

        # Create data display and input rows
        self.central_bearing_section.addLayout(create_data_input_row(self, self._inputs['Bearings']['eccentrics']['f'], 'f', 'Współczynnik tarcia tocznego', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['eccentrics']['di'], 'd', 'Średnica wewnętrzna łożyska', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['eccentrics']['do'], 'D', 'Średnica zewnętrzna łożyska', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_display_row(self, self._outputs['Bearings']['eccentrics']['drc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))

        # Create button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')

        self._select_central_bearing_rolling_element_button = DataButton('Wybierz elementy toczne')
        self._items['Bearings']['eccentrics']['rolling_elements'] = self._select_support_B_bearing_rolling_element_button

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_central_bearing_rolling_element_button)

        section_layout.addWidget(self.central_bearing_section)
        section_layout.addLayout(button_layout)
    
    def _change_section(self, index):
        self.stacked_sections.setCurrentIndex(index)
    
    def _enable_select_support_A_bearing_rolling_element_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        self._select_support_A_bearing_rolling_element_button.setEnabled(enable_button)

        if delete_choice:
            self._select_support_A_bearing_rolling_element_button.clear()

    def _enable_select_support_B_bearing_rolling_element_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        self._select_support_B_bearing_rolling_element_button.setEnabled(enable_button)

        if delete_choice:
            self._select_support_B_bearing_rolling_element_button.clear()
    
    def _enable_select_central_bearing_rolling_element_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        self._select_central_bearing_rolling_element_button.setEnabled(enable_button)

        if delete_choice:
            self._select_central_bearing_rolling_element_button.clear()
    
    def update_selected_support_A_bearing_rolling_element(self, item_data):
        """
        Update selected rolling element.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_support_A_bearing_rolling_element_button.setData(item_data)

    def update_selected_support_B_bearing_rolling_element(self, item_data):
        """
        Update selected rolling element.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_support_B_bearing_rolling_element_button.setData(item_data)

    def update_selected_central_bearing_rolling_element(self, item_data):
        """
        Update selected rolling element.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_central_bearing_rolling_element_button.setData(item_data)
    
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

        self._init_selector()
        self._init_sections()
        super().init_ui()
