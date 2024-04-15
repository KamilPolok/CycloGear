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

        self._init_tab_widget()
        self._init_function_buttons()

    def _init_tab_widget(self):
        '''
        Init widget holding and managing tabs.
        '''
        self._tab_widget = QTabWidget(self)
        self._tab_widget.currentChanged.connect(self._on_tab_change)

        self.tabs_section_layout.addWidget(self._tab_widget)

    def _init_function_buttons(self):
        '''
        Init next tab button and preview button.
        '''
        # Add button for opening next tab 
        self._next_tab_button = QPushButton('Dalej', self)
        self._next_tab_button.clicked.connect(self.next_tab)

        # Add button for opening the shaft designer
        self.preview_button = QPushButton('Podgląd', self)

        self.buttons_section_layout.addWidget(self._next_tab_button)
        self.buttons_section_layout.addWidget(self.preview_button)

    def _on_tab_change(self, tab_index):
        """
        Perform actions after a change of tabs.
        """
        if tab_index == self._tab_widget.count() - 1:
            self._next_tab_button.setDisabled(True)

    def init_tabs(self, tabs, tabs_titles):
        """
        Initialize tabs in the main window.
        """
        for tab, title in zip(tabs, tabs_titles):
            self._tab_widget.addTab(tab, title)
            tab.set_callback(self.update_access_to_next_tabs)
        
        # Disable all tabs except the first one
        for i in range(1, self._tab_widget.count()):
            self._tab_widget.setTabEnabled(i, False)

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
