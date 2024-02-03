from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QStackedWidget

from .TabIf import ITrackedTab, ITrackedWidget
from .TabCommon import create_data_display_row, create_data_input_row, format_value

from InputShaft.view.InputShaft import InputShaft

class Section(ITrackedWidget):
    def _init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

    def addLayout(self, layout):
        self.main_layout.addLayout(layout)
        self._setup_state_tracking()

class BearingsTab(ITrackedTab):
    updated_data_signal = pyqtSignal(dict)
    updated_support_A_bearing_data_signal = pyqtSignal(dict)
    updated_central_bearing_data_signal = pyqtSignal(dict)

    def _set_tab_data(self):
        """
        Set the initial data for the tab from the main parent's data.
        """
        attributes_to_acquire = ['LhA', 'fdA', 'ftA', 'Łożyska_podpora_A',
                                 'Lhc', 'fdc', 'ftc', 'Łożyska_centralne',]
        self.tab_data = {attr: self._parent.data[attr] for attr in attributes_to_acquire}
        self._items_to_select['Łożyska_podpora_A'] = ''
        self._items_to_select['Łożyska_centralne'] = ''

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
        self.layout_selector.addItems(["Podpora przesuwna A", "Wykorbienia"])
        self.layout_selector.currentIndexChanged.connect(self._change_section)
        self.main_layout.addWidget(self.layout_selector)

    def _init_sections(self):
        self.init_support_A_bearings_section()
        self.init_central_bearings_section()

        self.stacked_sections = QStackedWidget()
        self.stacked_sections.addWidget(self.support_A_bearing_section)
        self.stacked_sections.addWidget(self.central_bearing_section)

        self.main_layout.addWidget(self.stacked_sections)
    
    def init_support_A_bearings_section(self):
        """
        Create and layout the UI components for the support A bearing section.
        """
        self.support_A_bearing_section = Section(self, self._enable_select_support_A_bearings_button)

        # Create data display and input rows
        self.support_A_bearing_section.addLayout(create_data_display_row(self, 'dA', self._parent.data['dA'], 'd<sub>s</sub>', 'Średnica wewnętrzna'))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'LhA', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>'))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'ftA', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>'))
        self.support_A_bearing_section.addLayout(create_data_input_row(self, 'fdA', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>'))

        # Create button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')
        self._select_support_A_bearings_button = QPushButton('Wybierz łożysko')
        self._select_support_A_bearings_button.setEnabled(False)
        self._select_support_A_bearings_button.clicked.connect(self.update_selected_support_A_bearing_data)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_A_bearings_button)
        self.support_A_bearing_section.addLayout(button_layout)

    def init_central_bearings_section(self):
        """
        Create and layout the UI components for the central bearings section.
        """
        self.central_bearing_section = Section(self, self._enable_select_central_bearings_button)

        # Create data display and input rows
        self.central_bearing_section.addLayout(create_data_display_row(self, 'de', self._parent.data['de'], 'd<sub>e</sub>', 'Średnica wewnętrzna'))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'Lhc', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>'))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'ftc', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>'))
        self.central_bearing_section.addLayout(create_data_input_row(self, 'fdc', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>'))

        # Create button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_central_bearings_button = QPushButton('Wybierz łożysko')
        self._select_central_bearings_button.setEnabled(False)
        self._select_central_bearings_button.clicked.connect(self.update_selected_central_bearing_data)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_central_bearings_button)
        self.central_bearing_section.addLayout(button_layout)
    
    def _change_section(self, index):
        self.stacked_sections.setCurrentIndex(index)
    
    def _enable_select_support_A_bearings_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """

        if enable_button:
            self._select_support_A_bearings_button.setEnabled(True)
            if delete_choice:
                self._select_support_A_bearings_button.setText('Wybierz Łożysko')
                self._items_to_select['Łożyska_podpora_A'] = ''
                self._check_state()
        else:
            self._select_support_A_bearings_button.setEnabled(False)
    
    def _enable_select_central_bearings_button(self, enable_button, delete_choice):
        """
        Enable or disable the selection button based on whether all inputs are filled.
        """

        if enable_button:
            self._select_central_bearings_button.setEnabled(True)
            if delete_choice:
                self._select_central_bearings_button.setText('Wybierz Łożysko')
                self._items_to_select['Łożyska_centralne'] = ''
                self._check_state()
        else:
            self._select_central_bearings_button.setEnabled(False)
    
    def update_viewed_support_A_bearing_code(self, itemData):
        """
        Update the displayed code for the selected bearing.

        Args:
            itemData (dict): Data of the selected item.
        """
        self._select_support_A_bearings_button.setText(str(itemData['Kod'][0]))
        self.tab_data['Łożyska_podpora_A'] = itemData

        self._items_to_select['Łożyska_podpora_A'] = str(itemData['Kod'][0])
        self._check_state()

    def update_viewed_central_bearings_code(self, itemData):
        """
        Update the displayed code for the selected bearing.

        Args:
            itemData (dict): Data of the selected item.
        """
        self._select_central_bearings_button.setText(str(itemData['Kod'][0]))
        self.tab_data['Łożyska_centralne'] = itemData

        self._items_to_select['Łożyska_centralne'] = str(itemData['Kod'][0])
        self._check_state()
    
    def getData(self):
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
    
    def update_selected_support_A_bearing_data(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.getData()
        self.updated_support_A_bearing_data_signal.emit(tab_data)

    def update_selected_central_bearing_data(self):
        """
        Emit a signal with the updated data for the selected bearing.
        """
        tab_data = self.getData()
        self.updated_central_bearing_data_signal.emit(tab_data)

    def update_data(self):
        """
        Emit a signal with the updated data from the tab.
        """
        tab_data = self.getData()
        self.updated_data_signal.emit(tab_data)
    
    def update_tab(self):
        """
        Update the tab with data from the parent.
        """
        for key, value in self.output_values.items():
            if value != self._parent.data[key][0]:
                value = self._parent.data[key][0]
                self.output_values[key].setText(format_value(value))
