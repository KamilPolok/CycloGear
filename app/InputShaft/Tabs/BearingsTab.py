from copy import deepcopy

from PyQt6.QtCore import pyqtSignal
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

class BearingsTab(ITrackedTab):
    update_data_signal = pyqtSignal(dict)
    select_support_A_bearing_signal = pyqtSignal(dict)
    select_support_B_bearing_signal = pyqtSignal(dict)
    select_central_bearing_signal = pyqtSignal(dict)

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
        self.support_A_bearing_section.addLayout(create_data_display_row(self, 'dA', self.data['dA'], 'd<sub>s</sub>', 'Średnica wewnętrzna', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'LhA', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>', decimal_precision=0))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'ftA', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>', decimal_precision=2))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'fdA', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>', decimal_precision=2))

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_support_A_bearing_button = DataButton('Wybierz łożysko')
        self._items['Łożyska_podpora_A'] = self._select_support_A_bearing_button
        self._select_support_A_bearing_button.clicked.connect(self._select_support_A_bearing)

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
        self.support_B_bearing_section.addLayout(create_data_display_row(self, 'dB', self.data['dB'], 'd<sub>s</sub>', 'Średnica wewnętrzna', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'LhB', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>', decimal_precision=0))
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'ftB', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>', decimal_precision=2))
        self.support_B_bearing_section.addLayout(create_data_input_row(self, 'fdB', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>', decimal_precision=2))

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_support_B_bearing_button = DataButton('Wybierz łożysko')
        self._items['Łożyska_podpora_B'] = self._select_support_B_bearing_button
        self._select_support_B_bearing_button.clicked.connect(self._select_support_B_bearing)

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
        self.central_bearing_section.addLayout(create_data_display_row(self, 'de', self.data['de'], 'd<sub>e</sub>', 'Średnica wewnętrzna', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'Lhc', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>', decimal_precision=0))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'ftc', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>', decimal_precision=2))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'fdc', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>', decimal_precision=2))

        # Set button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_central_bearing_button = DataButton('Wybierz łożysko')
        self._items['Łożyska_centralne'] = self._select_central_bearing_button
        self._select_central_bearing_button.clicked.connect(self._select_central_bearing)

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
        self._select_support_A_bearing_button.setEnabled(enable_button)

        if delete_choice:
            self._select_support_A_bearing_button.clear()

    def _enable_select_support_B_bearing_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        self._select_support_B_bearing_button.setEnabled(enable_button)

        if delete_choice:
            self._select_support_B_bearing_button.clear()

    def _enable_select_central_bearing_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """
        self._select_central_bearing_button.setEnabled(enable_button)

        if delete_choice:
            self._select_central_bearing_button.clear()

    def _select_support_A_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self.select_support_A_bearing_signal.emit(tab_data)

    def _select_support_B_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self.select_support_B_bearing_signal.emit(tab_data)

    def _select_central_bearing(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.get_data()
        self.select_central_bearing_signal.emit(tab_data)
    
    def _emit_tab_data(self):
        """
        Emit a signal to update the data withe tab's one.
        """
        tab_data = self.get_data()
        self.update_data_signal.emit(tab_data)
    
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
        for attribute in self._outputs.keys():
            new_value = self.data[attribute][0]
            self._outputs[attribute].setValue(new_value)

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

        self.update_selected_support_A_bearing(data['Łożyska_podpora_A'])
        self.update_selected_support_B_bearing(data['Łożyska_podpora_B'])
        self.update_selected_central_bearing(data['Łożyska_centralne'])
    
    def init_data(self, data):
        """
        Override parent method. Set the initial data for the tab from the parent's data.

        Args:
            data (dict): Component data.
        """
        super().init_data(data)
        attributes_to_acquire = ['LhA', 'fdA', 'ftA',
                                 'LhB', 'fdB', 'ftB', 
                                 'Lhc', 'fdc', 'ftc']
        self.tab_data = {attr: deepcopy(self.data[attr]) for attr in attributes_to_acquire}
        self._items = {}
    
    def init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self._init_selector()
        self._init_sections()
        super().init_ui()
