from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton

from ShaftDesigner.controller.ShaftDesignerController import ShaftDesignerController
from ShaftDesigner.view.ShaftDesigner import ShaftDesigner

class MainWindow(QMainWindow):
    """
    Main window class for the application.
    """
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def set_data(self, data):
        """
        Set data needed for or from GUI.
        """
        self.data = data

    def set_shaft_designer_data(self, data):
        """
        Set data for the shaft designer
        """
        self.shaft_designer_controller.set_initial_data(data)

    def _init_ui(self):
        """
        Initialize the user interface.
        """
        # Set window attributes
        self.setWindowTitle('CycloDesign')

        # Set central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set layouts 
        self.main_layout = QVBoxLayout(central_widget)

        self.tabs_section_layout = QVBoxLayout()
        self.buttons_section_layout = QVBoxLayout()

        self.main_layout.addLayout(self.tabs_section_layout)
        self.main_layout.addLayout(self.buttons_section_layout)

        # Init buttons
        # Add button for opening next tab 
        self._next_tab_button = QPushButton('Dalej', self)
        self._next_tab_button.clicked.connect(self.next_tab)

        # Add button for opening the shaft designer
        self.preview_button = QPushButton('Podgląd', self)
        self.preview_button.clicked.connect(self._open_shaft_designer)
        self.preview_button.setEnabled(False)

        self.buttons_section_layout.addWidget(self._next_tab_button)
        self.buttons_section_layout.addWidget(self.preview_button)

        # Init shaft designer
        self._init_shaft_designer()
    
    def init_tabs(self):
        """
        Initialize tabs in the main window.
        """
        from .Tabs.BearingsTab import BearingsTab
        from .Tabs.PreliminaryDataTab import PreliminaryDataTab
        from .Tabs.ResultsTab import ResultsTab
        from .Tabs.PowerLossTab import PowerLossTab
        
        self._tab_widget = QTabWidget(self)
        self.tabs = []

        # Add tabs
        tab1 = PreliminaryDataTab(self, self.update_access_to_next_tabs)
        self.tabs.append(tab1)
        self._tab_widget.addTab(tab1, 'Założenia wstępne')

        tab2 = BearingsTab(self, self.update_access_to_next_tabs)
        self.tabs.append(tab2)
        self._tab_widget.addTab(tab2, 'Dobór łożysk')

        tab3 = PowerLossTab(self, self.update_access_to_next_tabs)
        self.tabs.append(tab3)
        self._tab_widget.addTab(tab3, 'Straty Mocy')

        tab4 = ResultsTab(self, self.update_access_to_next_tabs)
        self.tabs.append(tab4)
        self._tab_widget.addTab(tab4, 'Wyniki obliczeń')
        
        # Disable all tabs except the first one
        for i in range(1, self._tab_widget.count()):
            self._tab_widget.setTabEnabled(i, False)

        self._tab_widget.currentChanged.connect(self.on_tab_change)

        self.tabs_section_layout.addWidget(self._tab_widget)

        # Check if the first tab is initially filled
        self.tabs[self._tab_widget.currentIndex()].check_state()

    def _init_shaft_designer(self):
        # Set an instance of shaft designer
        self.shaft_designer = ShaftDesigner()

        # Set an instance of shaft designer controller
        self.shaft_designer_controller = ShaftDesignerController(self.shaft_designer)

    def _open_shaft_designer(self):
        self.update_data()
        self.shaft_designer.show()

    def update_data(self):
        current_index = self._tab_widget.currentIndex()
        self.tabs[current_index].update_data()

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
            self.update_data()
            self._tab_widget.setCurrentIndex(next_index)

    def on_tab_change(self, index):
        """
        Handle tab change event.
        """
        # Check if all the inputs are provided
        self.tabs[index].check_state()
        # Update tab GUI
        self.tabs[index].update_tab()
        
    def update_access_to_next_tabs(self, enable_next_tab_button=False, disable_next_tabs=False):
        """
        Check and update the state of the next tab button.
        """
        if enable_next_tab_button:
            self._next_tab_button.setEnabled(True)
            self.preview_button.setEnabled(True)
        else:
            self._next_tab_button.setEnabled(False)
            self.preview_button.setEnabled(False)

        if disable_next_tabs:
            self.disable_next_tabs()

    def disable_next_tabs(self):
        """
        Disable all tabs following the current tab.
        """
        for i in range(self._tab_widget.currentIndex() + 1, self._tab_widget.count()):
            self._tab_widget.setTabEnabled(i, False)
