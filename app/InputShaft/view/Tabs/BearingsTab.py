from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QWidget

from .common.DataButton import DataButton
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

class BearingsTab(ITrackedTab):
    update_data_signal = pyqtSignal(dict)
    select_support_A_bearing_signal = pyqtSignal(dict)
    select_support_B_bearing_signal = pyqtSignal(dict)
    select_central_bearing_signal = pyqtSignal(dict)

    def _set_tab_data(self):
        """
        Set the initial data for the tab from the main parent's data.
        """
        attributes_to_acquire = ['LhA', 'fdA', 'ftA',
                                 'LhB', 'fdB', 'ftB', 
                                 'Lhc', 'fdc', 'ftc']
        self.tab_data = {attr: self._parent.data[attr] for attr in attributes_to_acquire}
        self._items = {}

    def _init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._set_tab_data()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self._init_selector()
        self._init_sections()

    def _init_selector(self):
        self.layout_selector = QComboBox()
        self.layout_selector.addItems(["Podpora przesuwna A", "Podpora nieprzesuwna B", "Wykorbienia"])
        self.layout_selector.currentIndexChanged.connect(self._change_section)
        self.main_layout.addWidget(self.layout_selector)

    def _init_sections(self):
        self.init_support_A_bearing_section()
        self.init_support_B_bearing_section()
        self.init_central_bearing_section()

        self.stacked_sections = QStackedWidget()
        self.stacked_sections.addWidget(self.section_A)
        self.stacked_sections.addWidget(self.section_B)
        self.stacked_sections.addWidget(self.section_central)

        self.main_layout.addWidget(self.stacked_sections)
    
    def init_support_A_bearing_section(self):
        """
        Create and layout the UI components for the support A bearing section.
        """
        section_layout = QVBoxLayout()

        self.section_A = QWidget()
        self.section_A.setLayout(section_layout)

        # Set content container
        self.support_A_bearing_section = Section(self, self._enable_select_support_A_bearing_button)

        # Set data display and input rows
        self.support_A_bearing_section.addLayout(create_data_display_row(self, 'dA', self._parent.data['dA'], 'd<sub>s</sub>', 'Średnica wewnętrzna', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'LhA', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>', decimal_precision=0))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'ftA', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'fdA', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>', decimal_precision=2))

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_support_A_bearing_button = DataButton('Wybierz łożysko')
        self._items['Łożyska_podpora_A'] = self._select_support_A_bearing_button
        self._select_support_A_bearing_button.clicked.connect(self.select_support_A_bearing)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_A_bearing_button)

        section_layout.addWidget(self.support_A_bearing_section)
        section_layout.addLayout(button_layout)
    
    def init_support_B_bearing_section(self):
        """
        Create and layout the UI components for the support A bearing section.
        """
        section_layout = QVBoxLayout()

        self.section_B = QWidget()
        self.section_B.setLayout(section_layout)

        # Set content container
        self.support_B_bearing_section = Section(self, self._enable_select_support_B_bearing_button)

        # Set data display and input rows
        self.support_B_bearing_section.addLayout(create_data_display_row(self, 'dB', self._parent.data['dB'], 'd<sub>s</sub>', 'Średnica wewnętrzna', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'LhB', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>', decimal_precision=0))
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'ftB', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'fdB', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>', decimal_precision=2))

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_support_B_bearing_button = DataButton('Wybierz łożysko')
        self._items['Łożyska_podpora_B'] = self._select_support_B_bearing_button
        self._select_support_B_bearing_button.clicked.connect(self.select_support_B_bearing)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_B_bearing_button)

        section_layout.addWidget(self.support_B_bearing_section)
        section_layout.addLayout(button_layout)

    def init_central_bearing_section(self):
        """
        Create and layout the UI components for the central bearings section.
        """
        section_layout = QVBoxLayout()

        self.section_central = QWidget()
        self.section_central.setLayout(section_layout)

        # Set content container
        self.central_bearing_section = Section(self, self._enable_select_central_bearing_button)

        # Set data display and input rows
        self.central_bearing_section.addLayout(create_data_display_row(self, 'de', self._parent.data['de'], 'd<sub>e</sub>', 'Średnica wewnętrzna', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'Lhc', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>', decimal_precision=0))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'ftc', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'fdc', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>', decimal_precision=2))

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_central_bearing_button = DataButton('Wybierz łożysko')
        self._items['Łożyska_centralne'] = self._select_central_bearing_button
        self._select_central_bearing_button.clicked.connect(self.select_central_bearing)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_central_bearing_button)

        section_layout.addWidget(self.central_bearing_section)
        section_layout.addLayout(button_layout)
    
    def _change_section(self, index):
        self.stacked_sections.setCurrentIndex(index)
    
    def _enable_select_support_A_bearing_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        if enable_button:
            self._select_support_A_bearing_button.setEnabled(True)
            if delete_choice:
                self._select_support_A_bearing_button.clear()
        else:
            self._select_support_A_bearing_button.setEnabled(False)
    
    def _enable_select_support_B_bearing_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        if enable_button:
            self._select_support_B_bearing_button.setEnabled(True)
            if delete_choice:
                self._select_support_A_bearing_button.clear()
        else:
            self._select_support_B_bearing_button.setEnabled(False)
    
    def _enable_select_central_bearing_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        if enable_button:
            self._select_central_bearing_button.setEnabled(True)
            if delete_choice:
                self._select_central_bearing_button.clear()
        else:
            self._select_central_bearing_button.setEnabled(False)
    
    def update_selected_support_A_bearing(self, item_data):
        """
        Update the displayed code for the selected bearing.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_support_A_bearing_button.setData(item_data)

    def update_selected_support_B_bearing(self, item_data):
        """
        Update the displayed code for the selected bearing.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_support_B_bearing_button.setData(item_data)

    def update_selected_central_bearing(self, item_data):
        """
        Update the displayed code for the selected bearing.

        Args:
            item_data (dict): Data of the selected item.
        """
        self._select_central_bearing_button.setData(item_data)
    
    def get_data(self):
        """
        Retrieve and format the data from the input fields.

        Returns:
            dict: The formatted data from the tab.
        """
        for attribute, input in self.input_values.items():
            text = input.text()
            value = None if text == "" else literal_eval(text)
            self.tab_data[attribute][0] = value

        for attribute, item in self._items.items():
            self.tab_data[attribute] = item.data()

        return self.tab_data
    
    def select_support_A_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self.select_support_A_bearing_signal.emit(tab_data)

    def select_support_B_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self.select_support_B_bearing_signal.emit(tab_data)

    def select_central_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self.select_central_bearing_signal.emit(tab_data)

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
        for key, value in self.output_values.items():
            if value != self._parent.data[key][0]:
                value = self._parent.data[key][0]
                self.output_values[key].setText(format_value(value))
