from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

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
        self.centralWidget().setLayout(QVBoxLayout())

        # Add Chart
        self.chart = Chart()
        self.centralWidget().layout().addWidget(self.chart)

    def update_data(self, data):
        # Init plots
        self.chart.init_plots(data)