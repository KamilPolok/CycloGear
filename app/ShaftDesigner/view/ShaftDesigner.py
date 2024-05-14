from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon 
from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QSizePolicy, QSpacerItem, QPushButton,
                             QVBoxLayout, QWidget, QScrollArea)

from ShaftDesigner.view.Chart.Chart import Chart
from ShaftDesigner.view.Chart.Chart_Plotter import Chart_Plotter
from ShaftDesigner.view.Chart.Chart_ShaftViewer import Chart_ShaftViewer

from ShaftDesigner.view.Chart.Utils.CheckboxDropdown import CheckboxDropdown

from config import APP_NAME, APP_ICON

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
        self.setWindowIcon(QIcon(APP_ICON))

        self.resize(800,500)

        # Set main layout
        self.main_widget = QWidget(self)
        self.main_widget.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
        }
        """)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.main_widget)

        self._init_toolbar()

        # Set content layout
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(0)
        self.main_layout.addLayout(self.content_layout)

        # Init content widgets
        self._init_sidebar()
        self._init_chart()

        # Add buttons to the toolbar
        self._set_toolbar_buttons()

        # Set initial view
        self.sidebar.setVisible(False)
    
    def _init_toolbar(self):
        # Create custom toolbar
        self.toolbar = QWidget(self)
        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar.setObjectName('toolbarWidget')
        self.toolbar.setStyleSheet("""
        QWidget#toolbarWidget {
            background-color: #ffffff;
        }
        """)
        self.toolbar.setFixedHeight(40)
        self.toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_layout.setSpacing(5)
        self.main_layout.addWidget(self.toolbar)

        # Create default style of toolbar buttons 
        self.toolbar_buttons_style = """                         
            QPushButton {
                background-color: transparent;
                color: black;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #66beb2;
                border: 1px solid #66beb2;
            }
            QPushButton:pressed {
                background-color: #51988e;
                border: 1px solid #51988e;
            }
            QPushButton:checked {
                background-color: #66beb2;
                border: 1px solid #66beb2;                     
            }
        """

    def _init_sidebar(self):
        # Set container for sidebar content
        self.container = QWidget()
        self.container.setObjectName("containerWidget")
        self.container.setStyleSheet("""
        QWidget#containerWidget {
            background-color: #ffffff;
        }
        """)
        self.sidebar_layout = QVBoxLayout(self.container)

        # Set a scroll area for the sidebar
        self.sidebar = QScrollArea()
        self.sidebar.setStyleSheet("""
        QScrollArea {
            background-color: #ffffff;
            border: none;
        }
        QScrollBar:vertical {
            border: none;
            background: white;
            width: 13px;
            margin: 10px 0 10px 0;
        }
        QScrollBar::handle:vertical {
            background: #b5b5b5;
            min-height: 20px;
            max-height: 80px;
            border-radius: 4px;
            width: 8px;
            margin-right: 5px
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;  /* Removes the buttons */
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """)
        self.sidebar.setWidgetResizable(True)
        self.sidebar.setWidget(self.container)
        self.sidebar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.sidebar.setFixedWidth(230)

        self.content_layout.addWidget(self.sidebar)

    def _init_chart(self):
        # Create chart
        self.chart = Chart()
        self.plotter = Chart_Plotter(self.chart)
        self.shaft_viewer = Chart_ShaftViewer(self.chart)

        # Set the focus policy to accept focus and then set focus to the canvas
        self.chart.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.chart.setFocus()

        self.content_layout.addWidget(self.chart)
    
    def _set_toolbar_buttons(self):
        # Set sidebar toggle button
        toggle_sidebar_button = QPushButton(self)
        toggle_sidebar_button.setCheckable(True)
        toggle_sidebar_button.setStyleSheet(self.toolbar_buttons_style)
        toggle_sidebar_button.setFixedSize(QSize(30, 30))
        toggle_sidebar_button.setIconSize(QSize(24, 24))
        toggle_sidebar_button.setIcon(QIcon(resource_path('icons//menu.png')))
        toggle_sidebar_button.setToolTip('Otwórz/zamknij pasek boczny')
        toggle_sidebar_button.clicked.connect(self.toggle_sidebar)
        self.toolbar_layout.addWidget(toggle_sidebar_button)

        # Set adjust view action
        fit_to_window_button = QPushButton(self)
        fit_to_window_button.setStyleSheet(self.toolbar_buttons_style)
        fit_to_window_button.setFixedSize(QSize(30, 30))
        fit_to_window_button.setIconSize(QSize(24, 24))
        fit_to_window_button.setIcon(QIcon(resource_path('icons//fit_to_window.png')))
        fit_to_window_button.setToolTip("Dopasuj widok")
        fit_to_window_button.clicked.connect(self.chart.reset_initial_view)
        self.toolbar_layout.addWidget(fit_to_window_button)

        # Set menu with plots to view
        self._plots_menu = CheckboxDropdown()
        self._plots_menu.setFixedSize(QSize(30, 30))
        self._plots_menu.setIconSize(QSize(24, 24))
        self._plots_menu.stateChanged.connect(self._update_plots)
        self._plots_menu.setIcon(resource_path('icons\plots.png'), 'Wyświetl wykresy momentów')
        self.toolbar_layout.addWidget(self._plots_menu)

        # Set menu with plots to view
        self._min_diameters_menu = CheckboxDropdown()
        self._min_diameters_menu.setFixedSize(QSize(30, 30))
        self._min_diameters_menu.setIconSize(QSize(24, 24))
        self._min_diameters_menu.stateChanged.connect(self._update_plots)
        self._min_diameters_menu.setIcon(resource_path('icons\min_diameter.png'), 'Wyświetl wykresy średnic minimalnych')
        self.toolbar_layout.addWidget(self._min_diameters_menu)

        # Set menu with dimensions to display
        self._dimensions_menu = CheckboxDropdown()
        self._dimensions_menu.setFixedSize(QSize(30, 30))
        self._dimensions_menu.setIconSize(QSize(24, 24))
        self._dimensions_menu.setIcon(resource_path('icons\dimensions.png'), 'Wyświetl wymiary')
        self._dimensions_menu.addItem('dimensions', 'Wymiary wału', 'Wyświetl wymiary wału', self._toggle_dimensions)
        self._dimensions_menu.addItem('coordinates', 'Współrzędne wału', 'Wyświetl współrzędne wału', self._toggle_coordinates)
        self.toolbar_layout.addWidget(self._dimensions_menu)
        
        # Set button for displaying bearings
        self._toggle_bearings_plot_button = QPushButton(self)
        self._toggle_bearings_plot_button.setStyleSheet(self.toolbar_buttons_style)
        self._toggle_bearings_plot_button.setFixedSize(QSize(30, 30))
        self._toggle_bearings_plot_button.setIconSize(QSize(24, 24))
        self._toggle_bearings_plot_button.setIcon(QIcon(resource_path('icons//bearing.png')))
        self._toggle_bearings_plot_button.setToolTip("Wyświetl łożyska")
        self._toggle_bearings_plot_button.setCheckable(True)
        self._toggle_bearings_plot_button.setEnabled(False)
        self._toggle_bearings_plot_button.clicked.connect(self._toggle_bearings)
        self.toolbar_layout.addWidget(self._toggle_bearings_plot_button)

        # Set button for confirming shaft project:
        self.confirm_draft_button = QPushButton(self)
        self.confirm_draft_button.setStyleSheet("""                         
            QPushButton {
                background-color: #fba9a9;
                border: 1px solid #fba9a9;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f97f7f;
                border: 1px solid #f97f7f;
            }
            QPushButton:pressed {
                background-color: #f97171;
                border: 1px solid #f97171;
            }
        """)
        font = QFont()
        font.setBold(True)
        self.confirm_draft_button.setFont(font)
        self.confirm_draft_button.setFixedSize(QSize(140, 30))
        self.confirm_draft_button.setIconSize(QSize(24, 24))
        self.confirm_draft_button.setIcon(QIcon(resource_path('icons//approve.png')))
        self.confirm_draft_button.setToolTip("Zatwierdź projekt wału")
        self.confirm_draft_button.setText("Zatwierdź Projekt")
        self.confirm_draft_button.setEnabled(False)
        self.toolbar_layout.addWidget(self.confirm_draft_button)

        spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.toolbar_layout.addSpacerItem(spacer)

    def _toggle_dimensions(self, is_checked):
        if is_checked:
            if self._toggle_bearings_plot_button.isChecked():
                self._toggle_bearings_plot_button.click()
            self.shaft_viewer.draw_shaft_dimensions()
        else:
            self.shaft_viewer.remove_shaft_dimensions()

    def _toggle_coordinates(self, is_checked):
        if is_checked:
            if self._toggle_bearings_plot_button.isChecked():
                self._toggle_bearings_plot_button.click()
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

    def append_section_to_sidebar(self, section):
        # Add section before spacer
        self.sidebar_layout.insertWidget(self.sidebar_layout.count()-1, section)

    def remove_section_from_sidebar(self, section):
        for index in range( self.sidebar_layout.count()):
            item =  self.sidebar_layout.itemAt(index)
            if item.widget() == section:
                # Remove the widget from the layout
                self.sidebar_layout.takeAt(index)
                # Hide the widget
                section.hide()
                # Optionally delete the widget
                section.deleteLater()
                break

    def set_draft_finished_title(self, is_finished):
        if is_finished:
            self.setWindowTitle(self._window_title + ' (Projekt Zatwierdzony)')
        else:
            self.setWindowTitle(self._window_title)

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def show(self):
        if self.isHidden():
            super().show()
        else:
             # Restore the window if it's minimized or in the back
            self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized)
            self.activateWindow()
            self.raise_()
