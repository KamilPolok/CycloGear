from copy import deepcopy

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QWidget

from .common.DataButton import DataButton
from .common.ITrackedWidget import ITrackedWidget
from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_display_row, create_data_input_row

from InputShaft.view.InputShaft import InputShaft

class Section(ITrackedWidget):
    def _init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def addLayout(self, layout):
        self.main_layout.addLayout(layout)
        self._setup_state_tracking()

    def insertLayout(self, idx, layout):
        self.main_layout.insertLayout(idx, layout)

class PowerLossTab(ITrackedTab):
    update_data_signal = pyqtSignal(dict)
    select_support_A_bearing_rolling_element_signal = pyqtSignal(dict)
    select_support_B_bearing_rolling_element_signal = pyqtSignal(dict)
    select_central_bearing_rolling_element_signal = pyqtSignal(dict)

    def _init_tab_data(self):
        """
        Set the initial data for the tab from the parent's data.
        """
        attributes_to_acquire = ['fA','fB', 'fc']
        self.tab_data = {attr: deepcopy(self._parent.data[attr]) for attr in attributes_to_acquire}
        self._items = {}

    def _init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._init_tab_data()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.top_comonent_layout = QVBoxLayout()
        self.sections_component_layout = QHBoxLayout()

        self.layout().addLayout(self.top_comonent_layout)
        self.layout().addLayout(self.sections_component_layout)

        self._init_selector()
        self._init_sections()

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
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'fA', 'Współczynnik tarcia tocznego', 'f', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_display_row(self, 'dwAc', self._parent.data['dwAc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))
        
        # Set button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')

        self._select_support_A_bearing_rolling_element_button = DataButton('Wybierz elementy toczne')
        self._items['Toczne_podpora_A'] = self._select_support_A_bearing_rolling_element_button
        self._select_support_A_bearing_rolling_element_button.clicked.connect(self._select_support_A_bearing_rolling_element)

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
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'fB', 'Współczynnik tarcia tocznego', 'f', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_display_row(self, 'dwBc', self._parent.data['dwBc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))
        
        # Set button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')

        self._select_support_B_bearing_rolling_element_button = DataButton('Wybierz elementy toczne')
        self._items['Toczne_podpora_B'] = self._select_support_B_bearing_rolling_element_button
        self._select_support_B_bearing_rolling_element_button.clicked.connect(self._select_support_B_bearing_rolling_element)

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
        self.central_bearing_section.addLayout(create_data_input_row(self, 'fc', 'Współczynnik tarcia tocznego', 'f', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_display_row(self, 'dwcc', self._parent.data['dwcc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))

        # Create button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')

        self._select_central_bearing_rolling_element_button = DataButton('Wybierz elementy toczne')
        self._items['Toczne_centralnych'] = self._select_support_B_bearing_rolling_element_button
        self._select_central_bearing_rolling_element_button.clicked.connect(self._select_central_bearing_rolling_element)

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
        if enable_button:
            self._select_support_A_bearing_rolling_element_button.setEnabled(True)
            if delete_choice:
                self._select_support_A_bearing_rolling_element_button.clear()
        else:
            self._select_support_A_bearing_rolling_element_button.setEnabled(False)

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


    def _select_support_A_bearing_rolling_element(self):
        """
        Emit a signal with the updated data for the selected rolling element.
        """
        tab_data = self.get_data()
        self.select_support_A_bearing_rolling_element_signal.emit(tab_data)

    def _select_support_B_bearing_rolling_element(self):
        """
        Emit a signal with the updated data for the selected rolling element.
        """
        tab_data = self.get_data()
        self.select_support_B_bearing_rolling_element_signal.emit(tab_data)

    def _select_central_bearing_rolling_element(self):
        """
        Emit a signal with the updated data for the selected rolling element.
        """
        tab_data = self.get_data()
        self.select_central_bearing_rolling_element_signal.emit(tab_data)

    def _emit_tab_data(self):
        """
        Emit a signal to update the data with the tab's one.
        """
        tab_data = self.get_data()
        self.update_data_signal.emit(tab_data)
    
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

    def get_data(self):
        """
        Retrieve data from the tab.

        Returns:
            dict: The formatted data from the tab.
        """
        for attribute, input in self._inputs.items():
            self.tab_data[attribute][0] = input.value()

        for attribute, item in self._items.items():
            self.tab_data[attribute] = item.data()

        return self.tab_data

    def update_state(self):
        """
        Update the tab with parent data.
        """
        addData = True
        for key_tuple, value_label in self._outputs.items():
            # Check if the key is a tuple (indicating a parent-child relationship)
            if isinstance(key_tuple, tuple):
                parent_key, attribute = key_tuple
                if parent_key in self._parent.data and attribute in self._parent.data[parent_key]:
                    addData = False
                    new_value = self._parent.data[parent_key][attribute][0]
                    value_label.setValue(new_value)
                                        
            else:
                # Handle keys without a parent
                attribute = key_tuple
                if attribute in self._parent.data:
                    new_value = self._parent.data[attribute][0]
                    value_label.setValue(new_value)

        if addData:
            self.support_A_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_A','Dw'), self._parent.data['Łożyska_podpora_A']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska', decimal_precision=2))
            self.support_A_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_A','Dz'), self._parent.data['Łożyska_podpora_A']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska', decimal_precision=2))
            self.support_B_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_B','Dw'), self._parent.data['Łożyska_podpora_B']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska', decimal_precision=2))
            self.support_B_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_B','Dz'), self._parent.data['Łożyska_podpora_B']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska', decimal_precision=2))
            self.central_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_centralne','Dw'), self._parent.data['Łożyska_centralne']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska', decimal_precision=2))
            self.central_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_centralne','Dz'), self._parent.data['Łożyska_centralne']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska', decimal_precision=2))
    
    def set_state(self, data):
        """
        Set tab's state.

        Args:
            data (dict): Data to set the state of the tab with.
        """
        for attribute, input in self._inputs.items():
            value = data[attribute][0]
            if value is not None:
                input.setValue(value)

        self.update_selected_support_A_bearing_rolling_element(data['Toczne_podpora_A'])
        self.update_selected_support_B_bearing_rolling_element(data['Toczne_podpora_B'])
        self.update_selected_central_bearing_rolling_element(data['Toczne_centralnych'])
