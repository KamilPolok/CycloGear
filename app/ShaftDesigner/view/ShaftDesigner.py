from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon , QAction
from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
                             QVBoxLayout, QWidget, QScrollArea, QToolBar)

from ShaftDesigner.view.Chart.Chart import Chart
from ShaftDesigner.view.Chart.Chart_Plotter import Chart_Plotter
from ShaftDesigner.view.Chart.Chart_ShaftViewer import Chart_ShaftViewer

from ShaftDesigner.view.Chart.Utils.CheckboxDropdown import CheckboxDropdown

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

        # Set main layout
        self.main_widget = QWidget(self)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        self._init_sidebar()
        self._init_chart()
        self._init_toolbar()

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
        
        self.scroll_area.setVisible(False)

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

        self.plotter = Chart_Plotter(self.chart)
        self.shaft_viewer = Chart_ShaftViewer(self.chart)

    def _init_toolbar(self):
        # Set toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.toolbar.toggleViewAction().setVisible(False)

        # Set sidebar toggle button
        toggle_sidebar_action = QAction(self)
        toggle_sidebar_action.setIcon(QIcon(resource_path('icons//menu.png')))
        toggle_sidebar_action.setToolTip('Otwórz/zamknij pasek boczny')
        toggle_sidebar_action.setCheckable(True)
        toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        self.toolbar.addAction(toggle_sidebar_action)

        # Set adjust view action
        fit_to_window_action = QAction(self)
        fit_to_window_action.setIcon(QIcon(resource_path('icons//fit_to_window.png')))
        fit_to_window_action.setToolTip("Dopasuj widok")
        fit_to_window_action.triggered.connect(self.chart.reset_initial_view)
        self.toolbar.addAction(fit_to_window_action)

        # Set menu with plots to view
        self._plots_menu = CheckboxDropdown()
        self._plots_menu.stateChanged.connect(self._update_plots)
        self._plots_menu.setIcon(resource_path('icons\plots.png'), 'Wyświetl wykresy momentów')
        self.toolbar.addWidget(self._plots_menu)

        # Set menu with plots to view
        self._min_diameters_menu = CheckboxDropdown()
        self._min_diameters_menu.stateChanged.connect(self._update_plots)
        self._min_diameters_menu.setIcon(resource_path('icons\min_diameter.png'), 'Wyświetl wykresy średnic minimalnych')
        self.toolbar.addWidget(self._min_diameters_menu)

        # Set menu with dimensions to display
        self._dimensions_menu = CheckboxDropdown()
        self._dimensions_menu.setIcon(resource_path('icons\dimensions.png'), 'Wyświetl wymiary')
        self._dimensions_menu.addItem('dimensions', 'Wymiary wału', 'Wyświetl wymiary wału', self._toggle_dimensions)
        self._dimensions_menu.addItem('coordinates', 'Współrzędne wału', 'Wyświetl współrzędne wału', self._toggle_coordinates)
        self.toolbar.addWidget(self._dimensions_menu)
        
        # Set button for displaying bearings
        self._toggle_bearings_plot_action = QAction(self)
        self._toggle_bearings_plot_action.setIcon(QIcon(resource_path('icons//bearing.png')))
        self._toggle_bearings_plot_action.setToolTip("Wyświetl łożyska")
        self._toggle_bearings_plot_action.setCheckable(True)
        self._toggle_bearings_plot_action.triggered.connect(self._toggle_bearings)
        self.toolbar.addAction(self._toggle_bearings_plot_action)

    def _toggle_dimensions(self, is_checked):
        if is_checked:
            if self._toggle_bearings_plot_action.isChecked():
                self._toggle_bearings_plot_action.trigger()
            self.shaft_viewer.draw_shaft_dimensions()
        else:
            self.shaft_viewer.remove_shaft_dimensions()

    def _toggle_coordinates(self, is_checked):
        if is_checked:
            if self._toggle_bearings_plot_action.isChecked():
                self._toggle_bearings_plot_action.trigger()
            self.shaft_viewer.draw_shaft_coordinates()
        else:
            self.shaft_viewer.remove_shaft_coordinates()

    def _toggle_bearings(self, is_checked):
        if is_checked:
            for id in self._dimensions_menu.getCheckedItems():
                self._dimensions_menu.checkItem(id, False)
            self.shaft_viewer.draw_bearings()            
        else:
            self.shaft_viewer.remove_bearings()

    def _update_plots(self):
        selected_plots = self._plots_menu.getCheckedItems() + self._min_diameters_menu.getCheckedItems()
        self.plotter.set_selected_plots(selected_plots)

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
