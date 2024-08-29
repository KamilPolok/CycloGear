from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from config import RESOURCES_DIR_NAME, dependencies_path

class InputShaft(QWidget):
    show_preview_signal = pyqtSignal()
    """
    GUI class for the Input Shaft component.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()

        self.is_shaft_designed = False

    def _init_ui(self):
        """
        Initialize the user interface.
        """
        # Set layouts 
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.tabs_section_layout = QVBoxLayout()
        self.tabs_section_layout.setContentsMargins(0, 0, 0, 0)
        self.navigation_buttons_layout = QHBoxLayout()
        self.navigation_buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addLayout(self.tabs_section_layout)
        self.main_layout.addLayout(self.navigation_buttons_layout)

        # Set content
        self._init_tab_widget()
        self._init_function_buttons()

    def _init_tab_widget(self):
        '''
        Init widget holding and managing tabs.
        '''
        self._tab_widget = QTabWidget(self)

        self.tabs_section_layout.addWidget(self._tab_widget)

    def _init_function_buttons(self):
        '''
        Init previous tab button, next tab button and preview button.
        '''
        # Create button for moving to previous tab 
        self._previous_tab_button = QPushButton(self)
        self._previous_tab_button.setFixedSize(QSize(30, 30))
        self._previous_tab_button.setIcon(QIcon(dependencies_path(f'{RESOURCES_DIR_NAME}//icons//buttons//previous_icon.png')))
        self._previous_tab_button.setToolTip('Poprzednia zakładka')
        self._previous_tab_button.setIconSize(QSize(25, 18))
        self._previous_tab_button.clicked.connect(self._open_previous_tab)

        # Create button for moving to next tab 
        self._next_tab_button = QPushButton(self)
        self._next_tab_button.setFixedSize(QSize(30, 30))
        self._next_tab_button.setIcon(QIcon(dependencies_path(f'{RESOURCES_DIR_NAME}//icons//buttons//next_icon.png')))
        self._next_tab_button.setToolTip('Następna zakładka')
        self._next_tab_button.setIconSize(QSize(25, 18))
        self._next_tab_button.clicked.connect(self._open_next_tab)

        # Create button for opening the shaft preview
        self.preview_button = QPushButton('Podgląd', self)
        self.preview_button.setToolTip('Otwórz podgląd wału')
        self.preview_button.setFixedSize(QSize(100, 30))
        font = QFont('Segoe UI', 12)
        font.setBold(True)
        self.preview_button.setFont(font)

        distance_between_buttons = 10
        self.navigation_buttons_layout.setSpacing(distance_between_buttons)

        self.navigation_buttons_layout.addStretch(1)
        self.navigation_buttons_layout.addWidget(self._previous_tab_button)
        self.navigation_buttons_layout.addWidget(self.preview_button)
        self.navigation_buttons_layout.addWidget(self._next_tab_button)
        self.navigation_buttons_layout.addStretch(1)

    def _open_next_tab(self):
        """
        Move to the next tab.
        """
        next_index = self._tab_widget.currentIndex() + 1

        if next_index < self._tab_widget.count():
            self._tab_widget.setTabEnabled(next_index, True)
            self._tab_widget.setCurrentIndex(next_index)
    
    def _open_previous_tab(self):
        """
        Move to the previous tab.
        """
        previous_index = self._tab_widget.currentIndex() - 1

        if previous_index >= 0:
            self._tab_widget.setCurrentIndex(previous_index)

    def _on_tab_change(self, tab_index = 0):
        """
        Perform actions after a change of tabs.
        """
        # Perform actions uppon the tab activation
        self._tab_widget.currentWidget().on_activated()

        # Disable the next tab button if the current tab is the last one
        if tab_index == self._tab_widget.count() - 1:
            self._next_tab_button.setEnabled(False)

        # Toggle the visibility of the previous tab button
        if tab_index == 0:
            self._previous_tab_button.setEnabled(False)
        else:
            self._previous_tab_button.setEnabled(True)

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
        
        # Connect change of the tabs in the tab_widget to the _on_tab_change method
        self._tab_widget.currentChanged.connect(self._on_tab_change)

        # Check first tab after app initialization
        self._on_tab_change()

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
