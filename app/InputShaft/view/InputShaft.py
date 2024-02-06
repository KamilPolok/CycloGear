from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QPushButton

class InputShaft(QWidget):
    show_preview_signal = pyqtSignal()
    """
    GUI class for the Input Shaft component.
    """
    def __init__(self):
        super().__init__()
        self._init_ui()

        self.is_shaft_designed = False
    
    def set_data(self, data):
        """
        Set data needed for or from GUI.
        """
        self.data = data

    def _init_ui(self):
        """
        Initialize the user interface.
        """
        # Set layouts 
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

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

        self.buttons_section_layout.addWidget(self._next_tab_button)
        self.buttons_section_layout.addWidget(self.preview_button)
    
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

        self.tabs_section_layout.addWidget(self._tab_widget)

    def next_tab(self):
        """
        Move to the next tab.
        """
        next_index = self._tab_widget.currentIndex() + 1

        if next_index < self._tab_widget.count():
            self._tab_widget.setTabEnabled(next_index, True)
            self._tab_widget.setCurrentIndex(next_index)
        
    def update_access_to_next_tabs(self, enable_next_tab_button, disable_next_tabs):
        """
        Check and update the state of the next tab button.
        """
        self.enable_preview_button(enable_next_tab_button)

        if self.is_shaft_designed and enable_next_tab_button:
            self._next_tab_button.setEnabled(True)
        else:
            self._next_tab_button.setEnabled(False)

        if disable_next_tabs:
            self.disable_next_tabs()
    
    def enable_preview_button(self, enable):
        """
        Toggle the preview button visibility.

        Args:
            enable (bool): Specifies whether the preview button should be enabled (True) or disabled (False).
        """
        if self._tab_widget.currentIndex() == 0:
            self.preview_button.setEnabled(enable)

    def disable_next_tabs(self):
        """
        Disable all tabs following the current tab.
        """
        for i in range(self._tab_widget.currentIndex() + 1, self._tab_widget.count()):
            self._tab_widget.setTabEnabled(i, False)
    
    def handle_shaft_designing_finished(self):
        """
        This method is called when the shaft design is confirmed. It sets the
        first tab as current tab and updates the acces to next tabs.
        """
        self.is_shaft_designed = True
        self._tab_widget.setCurrentIndex(0)
        self.update_access_to_next_tabs(True, True)
