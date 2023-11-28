from ast import literal_eval
from abc import ABCMeta, abstractmethod
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QScrollArea
)

from ChartView import Chart

class MainWindow(QMainWindow):
    """
    Main window class for the application.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def set_data(self, data):
        """
        Set data needed for or from GUI.
        """
        self.data = data

    def set_chart_data(self, data):
        """
        Set data for the chart tab.
        """
        self.tabs[2].create_plots(data)

    def init_ui(self):
        """
        Initialize the user interface.
        """
        self.setWindowTitle('CycloDesign')
        self._tab_widget = QTabWidget(self)
        self.setCentralWidget(self._tab_widget)
    
    def init_tabs(self):
        """
        Initialize tabs in the main window.
        """
        self.tabs = []

        # Add tabs
        tab1 = PreliminaryDataTab(self, self.update_accsess_to_next_tabs)
        self.tabs.append(tab1)
        self._tab_widget.addTab(tab1, 'Założenia wstępne')

        tab2 = BearingsTab(self, self.update_accsess_to_next_tabs)
        self.tabs.append(tab2)
        self._tab_widget.addTab(tab2, 'Dobór łożysk')

        tab3 = ResultsTab(self, self.update_accsess_to_next_tabs)
        self.tabs.append(tab3)
        self._tab_widget.addTab(tab3, 'Wyniki obliczeń')

        # Disable all tabs except the first one
        for i in range(1, self._tab_widget.count()):
            self._tab_widget.setTabEnabled(i, False)

        self._tab_widget.currentChanged.connect(self.on_tab_change)

        # Add next tab button below the tabs
        self._next_tab_button = QPushButton('Dalej', self)
        self._next_tab_button.clicked.connect(self.next_tab)

        layout = QVBoxLayout()

        layout.addWidget(self._tab_widget)
        layout.addWidget(self._next_tab_button)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Check if the tab is initially filled
        self.tabs[self._tab_widget.currentIndex()].check_state()

    def next_tab(self):
        """
        Move to the next tab.
        """
        current_index = self._tab_widget.currentIndex()
        next_index = current_index + 1

        # Check if current tab is not the last one
        if next_index < self._tab_widget.count():
            # Enable next tab if it wasn't anabled earlier
            if not self._tab_widget.isTabEnabled(next_index):
                self._tab_widget.setTabEnabled(next_index, True)
            # Update data with curret tab data
            self.tabs[current_index].update_data()
            self._tab_widget.setCurrentIndex(next_index)

    def on_tab_change(self, index):
        """
        Handle tab change event.
        """
        # Check if all the inputs are provided
        self.tabs[index].check_state()
        # Update tab GUI
        self.tabs[index].update_tab()
        
    def update_accsess_to_next_tabs(self, enable_next_tab_button=False, disable_next_tabs=False):
        """
        Check and update the state of the next tab button.
        """
        if enable_next_tab_button:
            self._next_tab_button.setEnabled(True)
        else:
            self._next_tab_button.setEnabled(False)

        if disable_next_tabs:
            self.disable_next_tabs()

    def disable_next_tabs(self):
        """
        Disable all tabs following the current tab.
        """
        for i in range(self._tab_widget.currentIndex() + 1, self._tab_widget.count()):
            self._tab_widget.setTabEnabled(i, False)

class ABCQWidgetMeta(ABCMeta, type(QWidget)):
    pass

class Tab(QWidget, metaclass=ABCQWidgetMeta):
    def __init__(self, window: MainWindow, on_click_callback):
        """
        Initialize a base tab for the application.

        Args:
            window (MainWindow): The main window instance.
            on_click_callback (function): Callback function to be called on state change.
        """
        super().__init__()
        self._window = window
        self._on_click_callback = on_click_callback
        # Set the inputs list and dict - to track their state and verify if all inputs were provided in current tab 
        self._line_edits_states = {}
        self._items_to_select_states = {}
        # Set the dict of line edits that hold provided by user attribute values
        self.input_values = {}
        # Set the dict of (read only) line edits that hold displayed to user values 
        self.output_values = {}

        self.init_ui()
        self.setup_state_tracking()

    @abstractmethod
    def init_ui(self):
        """Initialize the user interface for the tab. Must be overridden in subclasses."""
        pass
    
    def update_tab(self):
        """Update the tab. This method can be overridden in subclasses to provide specific update logic."""
        pass
    
    def get_state(self):
        """
        Retrieve the current state of all inputs in the tab.

        Returns:
            list or None: A list of input states if all inputs are filled, otherwise None.
        """
        inputs_states = [line_edit.text() for line_edit in self._line_edits_states]
        inputs_states += [item for item in self._items_to_select_states.values()]
        return None if '' in inputs_states else inputs_states
    
    def setup_state_tracking(self):
        """
        Set up tracking for the state of input fields.
        Connects textChanged signals of QLineEdit widgets to the check_state method.
        """
        self._line_edits_states = self.findChildren(QLineEdit)
        
        for line_edit in self._line_edits_states:
            line_edit.textChanged.connect(self.check_state)

        self._original_state = self.get_state()

    def check_state(self):
        """
        Check the current state of inputs and invoke the callback function with appropriate arguments.
        This function is called whenever an input field's text is changed and on switching tab
        """
        current_state = self.get_state()
        all_filled = current_state is not None

        if all_filled:
            state_changed = current_state != self._original_state
            self._original_state = current_state
            self._on_click_callback(True, state_changed)
        else:
            self._on_click_callback(False, True)

class PreliminaryDataTab(Tab):
    updated_data_signal = pyqtSignal(dict)

    def _set_tab_data(self):
        """
        Initialize tab data from the main window's data.
        """
        attributes_to_acquire = ['L', 'L1', 'L2', 'LA', 'LB', 'Materiał', 'xz']
        self.tab_data = {attr: self._window.data[attr] for attr in attributes_to_acquire}
        self._items_to_select_states['Materiał'] = ''

    def init_ui(self):
        """
        Initialize the user interface for this tab.
        """
        self._set_tab_data()

        self.setLayout(QVBoxLayout())

        self._view_dimensions_component()
        self._view_material_stength_component()
        self._view_material_component()

    def _view_dimensions_component(self):
        """
        Create and layout the dimensions component of the tab.
        """
        component_layout = QVBoxLayout()
        component_label = QLabel('Wymiary:')

        shaft_length = create_data_input_row(self, 'L', 'Długość wału wejściowego', 'L')

        support_coordinates_label = QLabel('Współrzędne podpór:')
        pin_support = create_data_input_row(self, 'LA', 'Podpora stała A', 'L<sub>A</sub>')
        roller_support = create_data_input_row(self, 'LB', 'Podpora przesuwna B', 'L<sub>B</sub>')

        cyclo_disc_coordinates_label = QLabel('Współrzędne tarcz obiegowych:')
        cyclo_disc1 = create_data_input_row(self, 'L1', 'Tarcza obiegowa 1', 'L<sub>1</sub>')
        cyclo_disc2 = create_data_input_row(self, 'L2', 'Tarcza obiegowa 2', 'L<sub>2</sub>')

        component_layout.addWidget(component_label)
        component_layout.addLayout(shaft_length)
        component_layout.addWidget(support_coordinates_label)
        component_layout.addLayout(pin_support)
        component_layout.addLayout(roller_support)
        component_layout.addWidget(cyclo_disc_coordinates_label)
        component_layout.addLayout(cyclo_disc1)
        component_layout.addLayout(cyclo_disc2)

        self.layout().addLayout(component_layout)

    def _view_material_stength_component(self):
        """
        Create and layout the  component of the tab.
        """
        component_layout = QVBoxLayout()
        component_label = QLabel('Współczynnik bezpieczeństwa:')

        factor_of_safety = create_data_input_row(self, 'xz', '', 'x<sub>z</sub>')

        component_layout.addWidget(component_label)
        component_layout.addLayout(factor_of_safety)

        self.layout().addLayout(component_layout)

    def _view_material_component(self):
        """
        Create and layout the third co mponent of the tab.
        """
        component_layout = QHBoxLayout()
        component_label = QLabel('Materiał:')

        self.select_material_button = QPushButton('Wybierz Materiał')

        component_layout.addWidget(component_label)
        component_layout.addWidget(self.select_material_button)

        self.layout().addLayout(component_layout)

    def update_viewed_material(self, item_data):
        """
        Update the displayed material information.

        :param item_data: Dictionary containing material data.
        """
        self.select_material_button.setText(str(item_data['Oznaczenie'][0]))
        self.tab_data['Materiał'] = item_data

        self._items_to_select_states['Materiał'] = str(item_data['Oznaczenie'][0])
        self.check_state()

    def get_data(self):
        """
        Retrieve data from the input fields.

        :return: Dictionary of the tab's data.
        """
        for attribute, line_edit in self.input_values.items():
            text = line_edit.text()
            value = literal_eval(text)
            self.tab_data[attribute][0] = value

        return self.tab_data

    def update_data(self):
        """
        Emit a signal to update the tab's data.
        """
        tab_data = self.get_data()
        self.updated_data_signal.emit(tab_data)

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
        self._select_support_bearings_button.setText(str(itemData['kod'][0]))
        self.tab_data['Łożyska_podporowe'] = itemData

        self._items_to_select_states['Łożyska_podporowe'] = str(itemData['kod'][0])
        self.tab_data['ds'][0] = str(itemData['Dw'][0])
        self.check_state()

    def update_viewed_central_bearings_code(self, itemData):
        """
        Update the displayed code for the selected central bearing.

        Args:
            itemData (dict): Data of the selected item.
        """
        self._select_central_bearings_button.setText(str(itemData['kod'][0]))
        self.tab_data['Łożyska_centralne'] = itemData

        self._items_to_select_states['Łożyska_centralne'] = str(itemData['kod'][0])
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

class ResultsTab(Tab):
    def init_ui(self):
        """
        Initialize the user interface for ResultsTab.
        """
        self.setLayout(QVBoxLayout())
        
        self._subtab_widget = QTabWidget(self)
        self.layout().addWidget(self._subtab_widget)

        self.add_data_subtab()
        self.add_results_subtab()
        self.add_chart_subtab()

    def add_data_subtab(self):
        """
        Add a subtab for displaying data.
        """
        subtab = QScrollArea()
        subtab.setWidgetResizable(True)
        self._subtab_widget.addTab(subtab, 'Dane')

        content_widget = QWidget()
        self.data_subtab_layout = QVBoxLayout(content_widget)
        subtab.setWidget(content_widget)

        generalDataLabel = QLabel('Ogólne:')
        nwe = create_data_display_row(self, 'nwe', self._window.data['nwe'], 'n<sub>we</sub>', 'Prędkość obrotowa wejściowa')
        mwe = create_data_display_row(self, 'Mwe', self._window.data['Mwe'], 'M<sub>we</sub>', 'Moment obrotowy wejściowy')
        dimensionsLabel = QLabel('Wymiary:')
        l = create_data_display_row(self, 'L',  self._window.data['L'], 'L', 'Długość wału',)
        e = create_data_display_row(self, 'e',  self._window.data['e'], 'e', 'Mimośród')
        supportCoordinatesLabel = QLabel('Współrzędne podpór:')
        pinSupport = create_data_display_row(self, 'LA', self._window.data['LA'], 'L<sub>A</sub>', 'Podpora stała A',)
        rollerSupport = create_data_display_row(self, 'LB', self._window.data['LB'], 'L<sub>B</sub>', 'Podpora przesuwna B')
        cycloDiscCoordinatesLabel = QLabel('Współrzędne kół obiegowych:')
        cycloDisc1 = create_data_display_row(self, 'L1', self._window.data['L1'], 'L<sub>1</sub>', 'Tarcza obiegowa 1')
        cycloDisc2 = create_data_display_row(self, 'L2', self._window.data['L2'], 'L<sub>2</sub>', 'Tarcza obiegowa 2')
        materialsLabel = QLabel('Materiał:')
        
        self.data_subtab_layout.addWidget(generalDataLabel)
        self.data_subtab_layout.addLayout(nwe)
        self.data_subtab_layout.addLayout(mwe)
        self.data_subtab_layout.addWidget(dimensionsLabel)
        self.data_subtab_layout.addLayout(l)
        self.data_subtab_layout.addLayout(e)
        self.data_subtab_layout.addWidget(supportCoordinatesLabel)
        self.data_subtab_layout.addLayout(pinSupport)
        self.data_subtab_layout.addLayout(rollerSupport)
        self.data_subtab_layout.addWidget(cycloDiscCoordinatesLabel)
        self.data_subtab_layout.addLayout(cycloDisc1)
        self.data_subtab_layout.addLayout(cycloDisc2)
        self.data_subtab_layout.addWidget(materialsLabel)

    def add_results_subtab(self):
        """
        Add a subtab for displaying results.
        """
        subtab = QScrollArea()
        subtab.setWidgetResizable(True)
        self._subtab_widget.addTab(subtab, 'Wyniki')

        content_widget = QWidget()
        self.results_subtab_layout = QVBoxLayout(content_widget)
        subtab.setWidget(content_widget)

        dimensionsLabel = QLabel('Wymiary')
        ds = create_data_display_row(self, 'ds',  self._window.data['ds'], 'd<sub>s</sub>', 'Średnica wału')
        de = create_data_display_row(self, 'de',  self._window.data['de'], 'd<sub>e</sub>', 'Średnica wykorbienia')

        Łożyska1 = QLabel('Łożyska')

        self.results_subtab_layout.addWidget(dimensionsLabel)
        self.results_subtab_layout.addLayout(ds)
        self.results_subtab_layout.addLayout(de)
        self.results_subtab_layout.addWidget(Łożyska1)

    def add_chart_subtab(self):
        """
        Add a subtab for displaying charts.
        """
        self._chart_tab = Chart()
        self._subtab_widget.addTab(self._chart_tab, 'Wykresy')
    
    def create_plots(self, chart_data):
        """
        Create plots in the chart tab.

        :param chart_data: Data to be used for plotting.
        """
        self._chart_tab.create_plots(chart_data)

    def update_tab(self):
        addData = True 
        for key, value in self.output_values.items():
            if key in self._window.data and value != self._window.data[key][0]:
                value = self._window.data[key][0]
                self.output_values[key].setText(format_value(value))
            elif key in self._window.data['Materiał']:
                addData = False
                value = self._window.data['Materiał'][key][0]
                self.output_values[key].setText(format_value(value))
        
        if addData:
            for key, value in self._window.data['Materiał'].items():
                attribute = create_data_display_row(self, key, value, key)
                self.data_subtab_layout.addLayout(attribute)
            for key, value in self._window.data['Łożyska_podporowe'].items():
                attribute = create_data_display_row(self, key, value, key)
                self.results_subtab_layout.addLayout(attribute)
            for key, value in self._window.data['Łożyska_centralne'].items():
                attribute = create_data_display_row(self, key, value, key)
                self.results_subtab_layout.addLayout(attribute)
    
def create_data_input_row(tab: Tab, attribute: str, description: str, symbol: str) -> QHBoxLayout:
    """
    Create a row for data input with description, symbol, and input field.

    :param tab: The tab where the row will be added.
    :param attribute: The attribute name corresponding to the data.
    :param description: The description of the attribute.
    :param symbol: The symbol representing the attribute.
    :return: A QHBoxLayout containing the created widgets.
    """
    layout = QHBoxLayout()

    # Description label
    description_label = QLabel(description)
    description_label.setFixedWidth(150)
    description_label.setWordWrap(True)

    # Symbol label
    symbol_label = QLabel(f'{symbol} = ')
    symbol_label.setFixedWidth(50)

    # Line edit for input
    line_edit = QLineEdit()
    line_edit.setFixedWidth(80)
    if (value := tab.tab_data[attribute][0]) is not None:
        line_edit.setText(str(value))

    # Input validation
    regex = QRegularExpression('^(0|[1-9][0-9]{0,6})(\.[0-9]{1,4})?$')
    line_edit.setValidator(QRegularExpressionValidator(regex, line_edit))

    # Units label
    units_label = QLabel(tab.tab_data[attribute][-1])
    units_label.setFixedWidth(50)

    # Assemble the layout
    layout.addWidget(description_label)
    layout.addWidget(symbol_label)
    layout.addWidget(line_edit)
    layout.addWidget(units_label)

    # Save the line_edit for later reference
    tab.input_values[attribute] = line_edit

    return layout

def create_data_display_row(tab: Tab, attribute: str, data: list, symbol: str, description: str = '') -> QHBoxLayout:
    """
    Create a row for displaying data with description, symbol, and a read-only field.

    :param tab: The tab where the row will be added.
    :param attribute: The attribute name corresponding to the data.
    :param data: The data list containing the value and unit.
    :param symbol: The symbol representing the attribute.
    :param description: The description of the attribute.
    :return: A QHBoxLayout containing the created widgets.
    """
    layout = QHBoxLayout()

    # Description label
    description_label = QLabel(description)
    description_label.setFixedWidth(150)
    description_label.setWordWrap(True)

    # Symbol label
    symbol_label = QLabel(f'{symbol} = ')
    symbol_label.setFixedWidth(50)

    # Value label (read-only)
    value_label = QLineEdit(format_value(data[0]) if data[0] is not None else '')
    value_label.setReadOnly(True)
    value_label.setFixedWidth(80)

    # Units label
    units_label = QLabel(data[-1])
    units_label.setFixedWidth(50)

    layout.addWidget(description_label)
    layout.addWidget(symbol_label)
    layout.addWidget(value_label)
    layout.addWidget(units_label)

    # Save the label for later reference
    tab.output_values[attribute] = value_label
    return layout

def format_value(var) -> str:
    """
    Format a variable for display.

    :param var: The variable to format.
    :return: A string representation of the variable.
    """
    return f'{var:.2f}' if isinstance(var, float) else str(var)
