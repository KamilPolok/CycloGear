import mplcursors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)

from PyQt6.QtWidgets import QComboBox, QDialog, QVBoxLayout
from PyQt6.QtCore import Qt

class Chart(QDialog):
    """
    A class representing a chart widget in a PyQt application.

    This class is responsible for creating and managing the chart display,
    including the plot selection and updating the plot display.
    """
     
    def __init__(self):
        super().__init__()

        # Initialize the user interface for the chart widget
        self._init_ui()

        # Set the focus policy to accept focus and then set focus to the canvas
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.setFocus()

    def _init_ui(self):
        """
        Initialize the user interface components for the chart widget.
        """
        # Set window parameters
        self.setWindowTitle("Wał wejściowy - Podgląd")
        self.resize(800,500)

        # Set layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a matplotlib figure and canvas for plotting
        self._figure, self.ax = plt.subplots(constrained_layout=True)
        self.canvas = FigureCanvasQTAgg(self._figure)

        # Create a custom toolbar with plot selector
        self._toolbar = CustomToolbar(self.canvas, self)
        self._toolbar.active_plot_selector.currentTextChanged.connect(self._switch_plot)

        # Create and store the cursor object for interactive data display
        self.cursor = mplcursors.cursor(self.ax, hover=False)

        # Add the toolbar and canvas to the layout
        layout.addWidget(self._toolbar)
        layout.addWidget(self.canvas)

    def create_plots(self, data):
        """
        Create and store plot data from the provided data dictionary.

        :param data: A dictionary containing the data for the plots.
        """
        y = {
            'Mg': [data['Mg'], 'Mg(z)', 'Moment gnący Mg [Nm]'],
            'Ms': [data['Ms'], 'Ms(z)', 'Moment skręcający Ms [Nm]'],
            'Mz': [data['Mz'], 'Mz(z)', 'Moment zastępczy Mz [Nm]'],
            'dMz':  [data['dMz'], 'd(Mz)', 'Średnica minimalna ze względu na moment zastępczy dMz [mm]'],
            'dMs':  [data['dMs'], 'd(Ms)', 'Średnica minimalna ze względu na moment skręcający dMs [mm]'],
            'dqdop':  [data['dqdop'], 'd(q\')', 'Średnica minimalna ze względu na dopuszczalny kąt skręcenia dq\' [mm]'],
        }
        self._F = data['F']

        # Prepare plot data for each plot type
        self._plots = {value[1]: {
            'z': data['z'],
            'y': value[0],
            'title': value[1],
            'xlabel': 'Współrzędna z [mm]',
            'ylabel': value[2]
        } for key, value in y.items()}

        # Update the plot selector in the toolbar and connect the switch plot function
        self._toolbar.active_plot_selector.currentTextChanged.disconnect()
        self._toolbar.update_plot_selector([plot['title'] for plot in self._plots.values()])
        self._switch_plot(self._toolbar.active_plot_selector.currentText())
        self._toolbar.active_plot_selector.currentTextChanged.connect(self._switch_plot)
    
    def _switch_plot(self, selected_plot):
        """
        Switch the current plot based on the selected plot in the toolbar.

        :param selected_plot: The name of the plot to be displayed.
        """

        # Remove the annotations - this removes also cursor customization
        self.cursor.remove()

        # Get the selected plot info
        plot_info = self._plots[selected_plot]

        # Remove the previous plot
        self.ax.clear()

        # Plot the new one
        self.ax.plot(plot_info['z'], plot_info['y'], color='royalblue')
        self.ax.set_title(plot_info['title'], pad=7)
        self.ax.set_xlabel(plot_info['xlabel'])
        self.ax.set_ylabel(plot_info['ylabel'])
        self.ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='black')
        self.ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='gray')
        self.ax.minorticks_on()
        self.ax.autoscale_view()
        self.ax.set_xlim([0, plot_info['z'][-1]])

        # Reinitialize the cursor for the new plot
        self.cursor = mplcursors.cursor(self.ax, hover=False)
        self.cursor.connect("add", lambda sel: sel.annotation.set(
            text=f'({sel.target[0]:.2f}; {sel.target[1]:.2f})',
            fontsize=8,
            fontweight='bold',
            color='black',
            backgroundcolor='cornflowerblue',
            alpha=0.7
        ))
        self.canvas.draw()

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

        # Add a combo box for plot selection
        self.active_plot_selector = QComboBox()
        self.addWidget(self.active_plot_selector)

    def update_plot_selector(self, plots):
        """
        Update the plot selector with a list of plot names.

        :param plots: A list of plot names to be added to the plot selector.
        """
        self.active_plot_selector.clear()
        for plot in plots:
            self.active_plot_selector.addItem(plot)
