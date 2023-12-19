from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget,
                             QScrollArea)

from .Chart import Chart

class ShaftDesigner(QMainWindow):
    """
    A class representing chart and interface to design the shaft

    This class is responsible for comunication between chart and
    other components of the application and also for implementing
    the GUI for interactive shaft design
    """
    def __init__(self):
        super().__init__()

        self._init_ui()
    
    def _init_ui(self):
        # Set window parameters
        self.setWindowTitle("Wał Wejściowy")
        self.resize(800,500)

        # Set layout
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QHBoxLayout())

        self._init_sidebar()
        self._init_chart()

    def _init_sidebar(self):
        # Set sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar.setFixedWidth(200)  # Set the fixed width for the sidebar

        # Add a spacer item at the end of the sidebar layout - keeps the contents alignet to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.sidebar_layout .addSpacerItem(spacer)

        # Set a scroll area for the sidebar - make the sidebar scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sidebar)
        self.scroll_area.setFixedWidth(220)  # Slightly larger to accommodate scrollbar

        self.centralWidget().layout().addWidget(self.scroll_area)

    def _init_chart(self):
        # Add Chart
        self.chart = Chart()
        self.centralWidget().layout().addWidget(self.chart)

    def update_data(self, data):
        # Init plots
        self.chart.init_plots(data)