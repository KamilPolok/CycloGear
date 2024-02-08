from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget

from .common.ITrackedWidget import ITrackedWidget
from .common.ITrackedTab import ITrackedTab
from .common.common_functions import create_data_display_row, create_data_input_row, format_value

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

    def _set_tab_data(self):
        """
        Set the initial data for the tab from the parent's data.
        """
        attributes_to_acquire = ['fA','fB', 'fc','Toczne_podpora_A', 'Toczne_podpora_B', 'Toczne_centralnych']
        self.tab_data = {attr: self._parent.data[attr] for attr in attributes_to_acquire}
        self._items_to_select['Toczne_podpora_A'] = ''
        self._items_to_select['Toczne_podpora_B'] = ''
        self._items_to_select['Toczne_centralnych'] = ''

    def _init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._set_tab_data()

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
        self.stacked_sections.addWidget(self.support_A_bearing_section)
        self.stacked_sections.addWidget(self.support_B_bearing_section)
        self.stacked_sections.addWidget(self.central_bearing_section)

        self.main_layout.addWidget(self.stacked_sections)

    def _init_support_A_bearing_section(self):
        """
        Create and layout the UI components for the support A bearing section.
        """
        self.support_A_bearing_section = Section(self, self._enable_select_support_A_bearing_rolling_element_button)

        # Create data display and input rows
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'fA', 'Współczynnik tarcia tocznego', 'f', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_display_row(self, 'dwAc', self._parent.data['dwAc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))
        
        # Create button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')
        self._select_support_A_bearing_rolling_element_button = QPushButton('Wybierz elementy toczne')
        self._select_support_A_bearing_rolling_element_button.clicked.connect(self.select_support_A_bearing_rolling_element)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_A_bearing_rolling_element_button)
        self.support_A_bearing_section.addLayout(button_layout)

    def _init_support_B_bearing_section(self):
        """
        Create and layout the UI components for the support B bearing section.
        """
        self.support_B_bearing_section = Section(self, self._enable_select_support_B_bearing_rolling_element_button)

        # Create data display and input rows
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'fB', 'Współczynnik tarcia tocznego', 'f', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_display_row(self, 'dwBc', self._parent.data['dwBc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))
        
        # Create button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')
        self._select_support_B_bearing_rolling_element_button = QPushButton('Wybierz elementy toczne')
        self._select_support_B_bearing_rolling_element_button.clicked.connect(self.select_support_B_bearing_rolling_element)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_B_bearing_rolling_element_button)
        self.support_B_bearing_section.addLayout(button_layout)

    def _init_central_bearing_section(self):
        """
        Create and layout the UI components for the central bearing section.
        """
        self.central_bearing_section = Section(self, self._enable_select_central_bearing_rolling_element_button)

        # Create data display and input rows
        self.central_bearing_section.addLayout(create_data_input_row(self, 'fc', 'Współczynnik tarcia tocznego', 'f', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_display_row(self, 'dwcc', self._parent.data['dwcc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych', decimal_precision=2))

        # Create button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')
        self._select_central_bearing_rolling_element_button = QPushButton('Wybierz elementy toczne')
        self._select_central_bearing_rolling_element_button.clicked.connect(self.select_central_bearing_rolling_element)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_central_bearing_rolling_element_button)
        self.central_bearing_section.addLayout(button_layout)
    
    def _change_section(self, index):
        self.stacked_sections.setCurrentIndex(index)
    
    def _enable_select_support_A_bearing_rolling_element_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        if enable_button:
            self._select_support_A_bearing_rolling_element_button.setEnabled(True)
            if delete_choice:
                self._select_support_A_bearing_rolling_element_button.setText('Wybierz elementy toczne')
                self._items_to_select['Toczne_podpora_A'] = ''
                self._check_state()
        else:
            self._select_support_A_bearing_rolling_element_button.setEnabled(False)

    def _enable_select_support_B_bearing_rolling_element_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        if enable_button:
            self._select_support_B_bearing_rolling_element_button.setEnabled(True)
            if delete_choice:
                self._select_support_B_bearing_rolling_element_button.setText('Wybierz elementy toczne')
                self._items_to_select['Toczne_podpora_B'] = ''
                self._check_state()
        else:
            self._select_support_B_bearing_rolling_element_button.setEnabled(False)
    
    def _enable_select_central_bearing_rolling_element_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        if enable_button:
            self._select_central_bearing_rolling_element_button.setEnabled(True)
            if delete_choice:
                self._select_central_bearing_rolling_element_button.setText('Wybierz elementy toczne')
                self._items_to_select['Toczne_centralnych'] = ''
                self._check_state()
        else:
            self._select_central_bearing_rolling_element_button.setEnabled(False)
    
    def update_selected_support_A_bearing_rolling_element(self, item_data):
        """
        Update selected rolling element.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_support_A_bearing_rolling_element_button.setText(f"{self._parent.data['Łożyska_podpora_A']['elementy toczne'][0]} {str(item_data['Kod'][0])}")
        self.tab_data['Toczne_podpora_A'] = item_data

        self._items_to_select['Toczne_podpora_A'] = str(item_data['Kod'][0])
        self._check_state()

    def update_selected_support_B_bearing_rolling_element(self, item_data):
        """
        Update selected rolling element.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_support_B_bearing_rolling_element_button.setText(f"{self._parent.data['Łożyska_podpora_B']['elementy toczne'][0]} {str(item_data['Kod'][0])}")
        self.tab_data['Toczne_podpora_B'] = item_data

        self._items_to_select['Toczne_podpora_B'] = str(item_data['Kod'][0])
        self._check_state()

    def update_selected_central_bearing_rolling_element(self, item_data):
        """
        Update selected rolling element.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_central_bearing_rolling_element_button.setText(f"{self._parent.data['Łożyska_centralne']['elementy toczne'][0]} {str(item_data['Kod'][0])}")
        self.tab_data['Toczne_centralnych'] = item_data

        self._items_to_select['Toczne_centralnych'] = str(item_data['Kod'][0])
        self._check_state()
    
    def get_data(self):
        """
        Retrieve and format the data from the input fields.

        Returns:
            dict: The formatted data from the tab.
        """
        for attribute, line_edit in self.input_values.items():
            text = line_edit.text()
            value = None if text == "" else literal_eval(text)
            self.tab_data[attribute][0] = value
        return self.tab_data
    
    def select_support_A_bearing_rolling_element(self):
        """
        Emit a signal with the updated data for the selected rolling element.
        """
        tab_data = self.get_data()
        self.select_support_A_bearing_rolling_element_signal.emit(tab_data)

    def select_support_B_bearing_rolling_element(self):
        """
        Emit a signal with the updated data for the selected rolling element.
        """
        tab_data = self.get_data()
        self.select_support_B_bearing_rolling_element_signal.emit(tab_data)

    def select_central_bearing_rolling_element(self):
        """
        Emit a signal with the updated data for the selected rolling element.
        """
        tab_data = self.get_data()
        self.select_central_bearing_rolling_element_signal.emit(tab_data)

    def update_data(self):
        """
        Emit a signal with the updated data from the tab.
        """
        tab_data = self.get_data()
        self.update_data_signal.emit(tab_data)
    
    def update_tab(self):
        """
        Update the tab with data from the parent.
        """
        addData = True
        for key_tuple, value_label in self.output_values.items():
            # Check if the key is a tuple (indicating a parent-child relationship)
            if isinstance(key_tuple, tuple):
                parent_key, attribute = key_tuple
                if parent_key in self._parent.data and attribute in self._parent.data[parent_key]:
                    addData = False
                    new_value = self._parent.data[parent_key][attribute][0]
                    value_label.setText(format_value(new_value))
            else:
                # Handle keys without a parent
                attribute = key_tuple
                if attribute in self._parent.data:
                    new_value = self._parent.data[attribute][0]
                    value_label.setText(format_value(new_value))

        if addData:
            self.support_A_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_A','Dw'), self._parent.data['Łożyska_podpora_A']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska', decimal_precision=2))
            self.support_A_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_A','Dz'), self._parent.data['Łożyska_podpora_A']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska', decimal_precision=2))
            self.support_B_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_B','Dw'), self._parent.data['Łożyska_podpora_B']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska', decimal_precision=2))
            self.support_B_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_podpora_B','Dz'), self._parent.data['Łożyska_podpora_B']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska', decimal_precision=2))
            self.central_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_centralne','Dw'), self._parent.data['Łożyska_centralne']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska', decimal_precision=2))
            self.central_bearing_section.insertLayout(0, create_data_display_row(self, ('Łożyska_centralne','Dz'), self._parent.data['Łożyska_centralne']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska', decimal_precision=2))
