import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from PyQt6.QtWidgets import QCheckBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

from .Utils.CheckboxDropdown import CheckboxDropdown

class Chart(QWidget):
    """
    A class representing a chart widget in a PyQt application.

    This class is responsible for creating and managing the chart display,
    including the plot selection and updating the plot display.
    """
    def __init__(self, parent=None):
        super(Chart, self).__init__(parent)        
        # Initialize the user interface for the chart widget
        self._init_ui()

    def _init_ui(self):
        """
        Initialize the user interface components for the chart widget.
        """
        # Set layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a matplotlib figure and canvas for plotting
        figure, self._ax = plt.subplots(constrained_layout=True)

        # Set the display setting of the figure and axes
        background_color = 'white'
        figure.set_facecolor(background_color)
        self._ax.set_facecolor(background_color)

        # Remove axes ticks and spines and grid lines
        self._ax.set_xticks([])
        self._ax.set_yticks([])
        self._ax.spines[['right', 'top', 'bottom', 'left']].set_visible(False)
        self._ax.grid(False)

        self._canvas = FigureCanvas(figure)

        # Set the focus policy to accept focus and then set focus to the canvas
        self._canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._canvas.setFocus()

        # Create a custom toolbar with plot selector
        self._toolbar = CustomToolbar(self._canvas, self)

        # Add the toolbar and canvas to the layout
        layout.addWidget(self._toolbar)
        layout.addWidget(self._canvas)

    def get_chart_controls(self):
        return (self._ax, self._canvas, self._toolbar)

class CustomToolbar(NavigationToolbar):
    """
    A custom toolbar class for the chart widget, extending the NavigationToolbar.

    This class adds a plot selector as a combo box to the standard matplotlib toolbar.
    """

    def __init__(self, canvas, parent=None, coordinates=False):
        """
        Initialize the custom toolbar.

        :param canvas: The canvas associated with the toolbar.
        :param parent: The parent widget of the toolbar.
        :param coordinates: Flag to show coordinates on the toolbar.
        """
        super(CustomToolbar, self).__init__(canvas, parent, coordinates)

        # Prepare checkboxes dict for plot selection
        self.plots_selector = CheckboxDropdown()
        self.plots_selector.setTitle('f(z)')
        self.addWidget(self.plots_selector)

        # prepare checkbox for display dimensions
        self.show_dimensions_checkbox = QCheckBox('Wyświetl wymiary')
        self.addWidget(self.show_dimensions_checkbox)

    def add_plot(self, plot_name, plot_symbol):
        """
        Update the plot selector with a list of plot names.

        :param plot_name: Key of the plot
        :param plot_symbol: Symbol to view by the plots_selector

        """
        self.plots_selector.addItem(plot_symbol, plot_name)
