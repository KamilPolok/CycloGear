from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from .TabIf import Tab
from .TabCommon import create_data_display_row, create_data_input_row, format_value

from MainWindow.view.MainWindow import MainWindow

class BearingsTab(Tab):
    updated_data_signal = pyqtSignal(dict)
    updated_support_bearings_data_signal = pyqtSignal(dict)
    updated_central_bearings_data_signal = pyqtSignal(dict)

    def __init__(self, window: MainWindow, on_click_callback):
        """
        Initialize the BearingsTab with state tracking in the sublayouts.
        """
        super().__init__(window, on_click_callback)
        self.setup_sublayouts_state_tracking()

    def _set_tab_data(self):
        """
        Set the initial data for the tab from the main window's data.
        """
        attributes_to_acquire = ['Lhp', 'fdp', 'ftp', 'Łożyska_podporowe', 'ds',
                                 'Lhc', 'fdc', 'ftc', 'Łożyska_centralne', 'de',]
        self.tab_data = {attr: self._window.data[attr] for attr in attributes_to_acquire}
        self._items_to_select_states['Łożyska_podporowe'] = ''
        self._items_to_select_states['Łożyska_centralne'] = ''

    def init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._set_tab_data()

        self.setLayout(QVBoxLayout())

        self.component_layout = QHBoxLayout()
        self.layout().addLayout(self.component_layout)

        # Create UI sections for bearings
        self.view_support_bearings_section()
        self.view_central_bearings_section()

    def view_support_bearings_section(self):
        """
        Create and layout the UI components for the support bearings section.
        """
        self.support_bearings_section_layout = QVBoxLayout()
        section_label = QLabel('Łożyska podporowe:')

        # Create data display and input rows
        ds = create_data_display_row(self, 'dsc', self._window.data['dsc'], 'd<sub>s</sub>', 'Obliczona średnica wału wejściowego')
        lh = create_data_input_row(self, 'Lhp', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>')
        fd = create_data_input_row(self, 'ftp', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = create_data_input_row(self, 'fdp', 'Współczynnik zależny od temperatury pracy łożyska', 'f<sub>t</sub>')

        # Create button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')
        self._select_support_bearings_button = QPushButton('Wybierz łożysko')
        self._select_support_bearings_button.setEnabled(False)
        self._select_support_bearings_button.clicked.connect(self.update_selected_support_bearing_data)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_support_bearings_button)

        self.support_bearings_section_layout.addWidget(section_label)
        self.support_bearings_section_layout.addLayout(ds)
        self.support_bearings_section_layout.addLayout(lh)
        self.support_bearings_section_layout.addLayout(fd)
        self.support_bearings_section_layout.addLayout(ft)
        self.support_bearings_section_layout.addLayout(button_layout)

        self.component_layout.addLayout(self.support_bearings_section_layout)

    def view_central_bearings_section(self):
        """
        Create and layout the UI components for the central bearings section.
        """
        self.central_bearings_section_layout = QVBoxLayout()
        section_label = QLabel('Łożyska centralne:')

        # Create data display and input rows
        de = create_data_display_row(self, 'dec', self._window.data['dec'], 'd<sub>e</sub>', 'Obliczona średnica wykorbienia')
        lh = create_data_input_row(self, 'Lhc', 'Trwałość godzinowa łożyska', 'L<sub>h</sub>')
        fd = create_data_input_row(self, 'ftc', 'Współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = create_data_input_row(self, 'fdc', 'Współczynnik zależny od temperatury pracy', 'f<sub>t</sub>')

        # Create button for bearing selection
        button_layout = QHBoxLayout()
        button_label = QLabel('Łożysko:')

        self._select_central_bearings_button = QPushButton('Wybierz łożysko')
        self._select_central_bearings_button.setEnabled(False)
        self._select_central_bearings_button.clicked.connect(self.update_selected_central_bearing_data)

        button_layout.addWidget(button_label)
        button_layout.addWidget(self._select_central_bearings_button)

        self.central_bearings_section_layout.addWidget(section_label)
        self.central_bearings_section_layout.addLayout(de)
        self.central_bearings_section_layout.addLayout(lh)
        self.central_bearings_section_layout.addLayout(fd)
        self.central_bearings_section_layout.addLayout(ft)
        self.central_bearings_section_layout.addLayout(button_layout)

        self.component_layout.addLayout(self.central_bearings_section_layout)

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

        self.support_bearings_section_layout_original_state = self.get_layout_state(self._support_bearings_line_edits)
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
        state_changed = current_state != self.support_bearings_section_layout_original_state

        if all_filled:
            self.support_bearings_section_layout_original_state = current_state
            self._select_support_bearings_button.setEnabled(True)
            if state_changed:
                self._select_support_bearings_button.setText('Wybierz Łożysko')
                self._items_to_select_states['Łożyska_podporowe'] = ''
                self.check_state()
        else:
            self._select_support_bearings_button.setEnabled(False)
    
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
            self._select_central_bearings_button.setEnabled(True)
            if state_changed:
                self._select_central_bearings_button.setText('Wybierz Łożysko')
                self._items_to_select_states['Łożyska_centralne'] = ''
                self.check_state()
        else:
            self._select_central_bearings_button.setEnabled(False)
    
    def update_viewed_support_bearings_code(self, itemData):
        """
        Update the displayed code for the selected support bearing.

        Args:
            itemData (dict): Data of the selected item.
        """
        self._select_support_bearings_button.setText(str(itemData['Kod'][0]))
        self.tab_data['Łożyska_podporowe'] = itemData

        self._items_to_select_states['Łożyska_podporowe'] = str(itemData['Kod'][0])
        self.tab_data['ds'][0] = str(itemData['Dw'][0])
        self.check_state()

    def update_viewed_central_bearings_code(self, itemData):
        """
        Update the displayed code for the selected central bearing.

        Args:
            itemData (dict): Data of the selected item.
        """
        self._select_central_bearings_button.setText(str(itemData['Kod'][0]))
        self.tab_data['Łożyska_centralne'] = itemData

        self._items_to_select_states['Łożyska_centralne'] = str(itemData['Kod'][0])
        self.tab_data['de'][0] = str(itemData['Dw'][0])
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
    
    def update_selected_support_bearing_data(self):
        """
        Emit a signal with the updated data for the selected support bearing.
        """
        tab_data = self.getData()
        self.updated_support_bearings_data_signal.emit(tab_data)

    def update_selected_central_bearing_data(self):
        """
        Emit a signal with the updated data for the selected central bearing.
        """
        tab_data = self.getData()
        self.updated_central_bearings_data_signal.emit(tab_data)

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
        for key, value in self.output_values.items():
            if value != self._window.data[key][0]:
                value = self._window.data[key][0]
                self.output_values[key].setText(format_value(value))
