from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from .TabIf import Tab
from .TabCommon import create_data_display_row, create_data_input_row, format_value

from MainWindow.view.MainWindow import MainWindow

class PowerLossTab(Tab):
    updated_data_signal = pyqtSignal(dict)
    updated_support_bearings_rolling_element_data_signal = pyqtSignal(dict)
    updated_central_bearings_rolling_element_data_signal = pyqtSignal(dict)

    def __init__(self, window: MainWindow, on_click_callback):
        """
        Initialize the PowerLossTab with state tracking in the sublayouts.
        """
        super().__init__(window, on_click_callback)
        self.setup_sublayouts_state_tracking()

    def _set_tab_data(self):
        """
        Set the initial data for the tab from the main window's data.
        """
        attributes_to_acquire = ['f', 'Toczne_podporowych', 'Toczne_centralnych']
        self.tab_data = {attr: self._window.data[attr] for attr in attributes_to_acquire}
        self._items_to_select_states['Toczne_podporowych'] = ''
        self._items_to_select_states['Toczne_centralnych'] = ''

    def init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._set_tab_data()

        self.setLayout(QVBoxLayout())

        self.top_comonent_layout = QVBoxLayout()
        self.sections_component_layout = QHBoxLayout()

        self.layout().addLayout(self.top_comonent_layout)
        self.layout().addLayout(self.sections_component_layout)

        # Create UI sections for bearings
        self.view_top_component()
        self.view_support_bearings_section()
        self.view_central_bearings_section()
    
    def view_top_component(self):
        """
        Create and layout the UI components for the top component

        The other components do not depend on inputs in this component
        """
        f = create_data_input_row(self, 'f', 'Luz', 'f')

        self.top_comonent_layout.addLayout(f)

    def view_support_bearings_section(self):
        """
        Create and layout the UI components for the support bearings section.
        """
        self.support_bearings_section_layout = QVBoxLayout()
        section_label = QLabel('Łożyska podporowe:')

        # Create data display and input rows
        #rolling_element = create_data_display_row(self, ('Łożyska_podporowe','elementy toczne'), self._window.data['Łożyska_podporowe'], '', 'Elementy toczne')
        dw = create_data_display_row(self, 'dwpc', self._window.data['dwpc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych')
        
        # Create button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Elementy toczne:')
        self._select_support_bearings_rolling_element_button = QPushButton('Wybierz elementy toczne')
        self._select_support_bearings_rolling_element_button.setEnabled(False)
        self._select_support_bearings_rolling_element_button.clicked.connect(self.update_selected_support_bearings_rolling_element_data)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_bearings_rolling_element_button)

        self.support_bearings_section_layout.addWidget(section_label)
        # self.support_bearings_section_layout.addLayout(rolling_element)
        self.support_bearings_section_layout.addLayout(dw)
        self.support_bearings_section_layout.addLayout(button_layout)

        self.sections_component_layout.addLayout(self.support_bearings_section_layout)

    def view_central_bearings_section(self):
        """
        Create and layout the UI components for the central bearings section.
        """
        self.central_bearings_section_layout = QVBoxLayout()
        section_label = QLabel('Łożyska centralne:')

        # Create data display and input rows
        #rolling_element = create_data_display_row(self, ('Łożyska_centralne','elementy toczne'), self._window.data['Łożyska_centralne'], '', 'Elementy toczne')
        dw = create_data_display_row(self, 'dwcc', self._window.data['dwcc'], 'd<sub>w</sub>', 'Obliczona średnica elementów tocznych')

        # Create button for rolling element selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Element toczny:')
        self._select_central_bearings_rolling_element_button = QPushButton('Wybierz elementy toczne')
        self._select_central_bearings_rolling_element_button.setEnabled(False)
        self._select_central_bearings_rolling_element_button.clicked.connect(self.update_selected_central_bearings_rolling_element_data)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_central_bearings_rolling_element_button)

        self.central_bearings_section_layout.addWidget(section_label)
        # self.central_bearings_section_layout.addLayout(rolling_element)
        self.central_bearings_section_layout.addLayout(dw)
        self.central_bearings_section_layout.addLayout(button_layout)

        self.sections_component_layout.addLayout(self.central_bearings_section_layout)

    def get_layout_state(self, line_edits):
        """
        Get the current state of a layout based on the text in its line edits.

        Args:
            line_edits (list): List of QLineEdit objects.

        Returns:
            list/None: List of text from each QLineEdit if none are empty, else None.
        """
        layout_input_states = [line_edit.text() for line_edit in line_edits]
        return None if '' in layout_input_states else layout_input_states

    def setup_sublayouts_state_tracking(self):
        """
        Setup state tracking for the sublayouts in the tab.
        This involves identifying line edits in each section and setting up their initial state.
        """
        self._support_bearings_line_edits = [le for le in self._line_edits_states if self.is_widget_in_layout(le, self.support_bearings_section_layout)]
        self._central_bearings_line_edits = [le for le in self._line_edits_states if self.is_widget_in_layout(le, self.central_bearings_section_layout)]

        self._support_bearings_section_layout_original_state = self.get_layout_state(self._support_bearings_line_edits)
        self._central_bearings_section_layout_original_state = self.get_layout_state(self._central_bearings_line_edits)

        for line_edit in self._support_bearings_line_edits:
            line_edit.textChanged.connect(self.check_support_bearings_section_layout_state)

        for line_edit in self._central_bearings_line_edits:
            line_edit.textChanged.connect(self.check_central_bearings_section_layout_state)

    def is_widget_in_layout(self, widget, layout):
        """
        Check if a given widget is in a specified layout.

        Args:
            widget (QWidget): The widget to check.
            layout (QLayout): The layout to search within.

        Returns:
            bool: True if the widget is in the layout, False otherwise.
        """
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == widget:
                return True
            elif item.layout() and self.is_widget_in_layout(widget, item.layout()):
                return True
        return False
    
    def check_support_bearings_section_layout_state(self):
        """
        Check the state of the support bearings section layout and update the UI accordingly.
        Enables or disables the selection button based on whether all inputs are filled.
        """
        current_state = self.get_layout_state(self._support_bearings_line_edits)
        all_filled = current_state is not None
        state_changed = current_state != self._support_bearings_section_layout_original_state

        if all_filled:
            self._support_bearings_section_layout_original_state = current_state
            self._select_support_bearings_rolling_element_button.setEnabled(True)
            if state_changed:
                self._select_support_bearings_rolling_element_button.setText('Wybierz elementy toczne')
                self._items_to_select_states['Toczne_podporowych'] = ''
                self.check_state()
        else:
            self._select_support_bearings_rolling_element_button.setEnabled(False)
    
    def check_central_bearings_section_layout_state(self):
        """
        Check the state of the central bearings section layout and update the UI accordingly.
        Enables or disables the selection button based on whether all inputs are filled.
        """
        current_state = self.get_layout_state(self._central_bearings_line_edits)
        all_filled = current_state is not None
        state_changed = current_state != self._central_bearings_section_layout_original_state

        if all_filled:
            self._central_bearings_section_layout_original_state = current_state
            self._select_central_bearings_rolling_element_button.setEnabled(True)
            if state_changed:
                self._select_central_bearings_rolling_element_button.setText('Wybierz elementy toczne')
                self._items_to_select_states['Toczne_centralnych'] = ''
                self.check_state()
        else:
            self._select_central_bearings_rolling_element_button.setEnabled(False)
    
    def update_viewed_support_bearings_rolling_element_code(self, itemData):
        """
        Update the displayed code for the selected support bearing rolling element.

        Args:
            itemData (dict): Data of the selected item.
        """
        self._select_support_bearings_rolling_element_button.setText(f"{self._window.data['Łożyska_podporowe']['elementy toczne'][0]} {str(itemData['Kod'][0])}")
        self.tab_data['Toczne_podporowych'] = itemData

        self._items_to_select_states['Toczne_podporowych'] = str(itemData['Kod'][0])
        self.check_state()

    def update_viewed_central_bearings_rolling_element_code(self, itemData):
        """
        Update the displayed code for the selected central bearing rolling element.

        Args:
            itemData (dict): Data of the selected item.
        """
        self._select_central_bearings_rolling_element_button.setText(f"{self._window.data['Łożyska_centralne']['elementy toczne'][0]} {str(itemData['Kod'][0])}")
        self.tab_data['Toczne_centralnych'] = itemData

        self._items_to_select_states['Toczne_centralnych'] = str(itemData['Kod'][0])
        self.check_state()
    
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
    
    def update_selected_support_bearings_rolling_element_data(self):
        """
        Emit a signal with the updated data for the selected support bearing rolling element.
        """
        tab_data = self.getData()
        self.updated_support_bearings_rolling_element_data_signal.emit(tab_data)

    def update_selected_central_bearings_rolling_element_data(self):
        """
        Emit a signal with the updated data for the selected central bearing rolling element.
        """
        tab_data = self.getData()
        self.updated_central_bearings_rolling_element_data_signal.emit(tab_data)

    def update_data(self):
        """
        Emit a signal with the updated data from the tab.
        """
        tab_data = self.getData()
        self.updated_data_signal.emit(tab_data)
    
    def update_tab(self):
        """
        Update the tab with data from the main window.
        """
        addData = True
        for key_tuple, value_label in self.output_values.items():
            # Check if the key is a tuple (indicating a parent-child relationship)
            if isinstance(key_tuple, tuple):
                parent_key, attribute = key_tuple
                if parent_key in self._window.data and attribute in self._window.data[parent_key]:
                    addData = False
                    new_value = self._window.data[parent_key][attribute][0]
                    value_label.setText(format_value(new_value))
            else:
                # Handle keys without a parent
                attribute = key_tuple
                if attribute in self._window.data:
                    new_value = self._window.data[attribute][0]
                    value_label.setText(format_value(new_value))

        if addData:
            Dwp = create_data_display_row(self, ('Łożyska_centralne','Dw'), self._window.data['Łożyska_centralne']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska')
            Dzp = create_data_display_row(self, ('Łożyska_centralne','Dz'), self._window.data['Łożyska_centralne']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska')
            self.central_bearings_section_layout.insertLayout(0, Dzp)
            self.central_bearings_section_layout.insertLayout(0, Dwp)
            Dwc = create_data_display_row(self, ('Łożyska_podporowe','Dw'), self._window.data['Łożyska_podporowe']['Dw'], 'D<sub>w</sub>', 'Średnica wewnętrzna łożyska')
            Dzc = create_data_display_row(self, ('Łożyska_podporowe','Dz'), self._window.data['Łożyska_podporowe']['Dz'], 'D<sub>z</sub>', 'Średnica zewnętrzna łożyska')
            self.support_bearings_section_layout.insertLayout(0, Dwc)
            self.support_bearings_section_layout.insertLayout(0, Dzc)