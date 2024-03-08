from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon , QAction
from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStyle,
                             QVBoxLayout, QWidget, QScrollArea, QToolBar)

from ShaftDesigner.view.Chart.Chart import Chart
from ShaftDesigner.view.Chart.Chart_Plotter import Chart_Plotter
from ShaftDesigner.view.Chart.Chart_ShaftViewer import Chart_ShaftViewer

from config import APP_NAME

from config import resource_path
class ShaftDesigner(QMainWindow):
    """
    A class representing chart and interface to design the shaft

    This class is responsible for comunication between chart and
    other components of the application and also for implementing
    the GUI for interactive shaft design
    """
    def __init__(self, window_title):
        super().__init__()
        self._init_ui(window_title)
    
    def _init_ui(self, designed_part_name):
        # Set window parameters
        self._window_title = APP_NAME + ' - ' + designed_part_name
        self.setWindowTitle(self._window_title)
        self.resize(800,500)

        # Set toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.toolbar.toggleViewAction().setVisible(False)

        # Set main layout
        self.main_widget = QWidget(self)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        self._init_sidebar()
        self._init_chart()

    def _init_sidebar(self):
        # Set sidebar
        self.sidebar = QWidget()

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Set a scroll area for the sidebar - make the sidebar scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sidebar)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.scroll_area.setFixedWidth(220)  # Slightly larger to accommodate scrollbar

        self.main_layout.addWidget(self.scroll_area)

        # Set sidebar toggle button
        toggle_sidebar_action = QAction(self)
        toggle_sidebar_action.setIcon(QIcon(resource_path('icons//menu.png')))
        toggle_sidebar_action.setToolTip('Otwórz/zamknij pasek boczny')
        toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        self.toolbar.addAction(toggle_sidebar_action)

    def _init_chart(self):
        # Chart section layout
        self._chart_section_layout = QVBoxLayout()

        # Create chart
        self.chart = Chart()

        # Create confirmation button:
        self.confirmation_button = QPushButton('Zatwierdź Projekt')
        self.confirmation_button.setEnabled(False)

        self._chart_section_layout.addWidget(self.chart)
        self._chart_section_layout.addWidget(self.confirmation_button)

        self.main_layout.addLayout(self._chart_section_layout)

        # Add actions to the toolbar
        fit_to_window_action = QAction(self)
        fit_to_window_action.setIcon(QIcon(resource_path('icons//fit_to_window.png')))
        fit_to_window_action.setToolTip("Dopasuj widok")
        fit_to_window_action.triggered.connect(self.chart.reset_initial_view)
        self.toolbar.addAction(fit_to_window_action)

        self.plotter = Chart_Plotter(self.chart, self.toolbar)
        self.shaft_viewer = Chart_ShaftViewer(self.chart, self.toolbar)
        
    def set_sidebar_sections(self, sections):
        # Set contents of the sidebar
        for section in sections.values():
            self.sidebar_layout.addWidget(section)

        # Add a spacer item at the end of the sidebar layout - keeps the contents aligned to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.sidebar_layout.addSpacerItem(spacer)

    def set_draft_finished_title(self, is_finished):
        if is_finished:
            self.setWindowTitle(self._window_title + ' (Projekt Zatwierdzony)')
        else:
            self.setWindowTitle(self._window_title)

    def toggle_sidebar(self):
        self.scroll_area.setVisible(not self.scroll_area.isVisible())

    def show(self):
        if self.isHidden():
            super().show()
        else:
             # Restore the window if it's minimized or in the back
            self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized)
            self.activateWindow()
            self.raise_()
