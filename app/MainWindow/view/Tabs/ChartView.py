import mplcursors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)

from PyQt6.QtWidgets import QCheckBox, QDialog, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

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
        self._toolbar.updated_selected_plots.connect(self._update_plot)

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

        self._data = data

        # Set data for every plot
        y = {
            'Mg': [data['Mg'], 'Mg(z)', 'Moment gnący Mg [Nm]', 'blue'],
            'Ms': [data['Ms'], 'Ms(z)', 'Moment skręcający Ms [Nm]', 'green'],
            'Mz': [data['Mz'], 'Mz(z)', 'Moment zastępczy Mz [Nm]', 'orange'],
            'dMz':  [data['dMz'], 'd(Mz)', 'Średnica minimalna ze względu na moment zastępczy dMz [mm]', 'purple'],
            'dMs':  [data['dMs'], 'd(Ms)', 'Średnica minimalna ze względu na moment skręcający dMs [mm]', 'red'],
            'dqdop':  [data['dqdop'], 'd(q\')', 'Średnica minimalna ze względu na dopuszczalny kąt skręcenia dq\' [mm]', 'black'],
        }

        self._F = self._data['F']

        # Prepare z data
        self._z = {
            'z': self._data['z'],
            'zlabel': 'Współrzędna z [mm]',
        }

        # Prepare plot data for each plot type
        self._plots = {value[1]: {
            'y': value[0],
            'title': value[1],
            'ylabel': value[2],
            'color': value[3]
        } for key, value in y.items()}

        # Initialize variables to store the overall max and min values
        self.overall_max = float('-inf')
        self.overall_min = float('inf')

        for key in y:
            current_max = max(y[key][0])
            current_min = min(y[key][0])

            if current_max > self.overall_max:
                self.overall_max = current_max
            if current_min < self.overall_min:
                self.overall_min = current_min
        
        # Update the plot selector in the toolbar and connect the switch plot function
        self._toolbar.update_plot_selector([plot['title'] for plot in self._plots.values()])
        self._update_plot()
    
    def _draw_shaft_coordinates(self):
        roller_support = self._data['LA']
        pin_support = self._data['LB']
        eccentric1_position = self._data['L1']
        eccentric2_position = self._data['L2']
        shaft_length = self._data['L']


        # Define markers and corresponding labels
        markers = [roller_support, eccentric1_position, eccentric2_position, pin_support, shaft_length]
        labels = ['A', 'L1', 'L2', 'B', 'L']

        # Draw markers
        self.ax.scatter(markers, [0] * len(markers), color='black', s=8, zorder=5)

        # Add labels for the markers
        for marker, label in zip(markers, labels):
            self.ax.annotate(label, (marker, 0), textcoords="offset points", xytext=(0, -15), ha='center')
    
    def _update_plot(self):
        """
        Switch the current plot based on the selected plot in the toolbar.

        :param selected_plot: The name of the plot to be displayed.
        """
        # Remove the annotations - this removes also cursor customization
        self.cursor.remove()

        # Remove the previous plot
        self.ax.clear()

        # Draw shaft characteristic points
        self._draw_shaft_coordinates()

        # Set z and y axis limits
        offset = 0.1 * self._data['L']
        self.ax.set_xlim([0 - offset, self._data['L'] + offset])
        self.ax.set_ylim(self.overall_min + 0.2 * self.overall_min, self.overall_max + 0.2 * self.overall_max)
        self.ax.set_xlabel(self._z['zlabel'])
        self.ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='black')
        self.ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='gray')
        self.ax.minorticks_on()

        # Plot selected plots
        selected_plots = [key for key, checkbox in self._toolbar.checkboxes.items() if checkbox.isChecked()]

        for plot_name in selected_plots:
            plot_info = self._plots[plot_name]
            if plot_name.lower().startswith('d'):
                self.ax.plot(self._z['z'], plot_info['y'], color=plot_info['color'])
            else:
                markerline, stemline, baseline = self.ax.stem(self._z['z'], plot_info['y'], linefmt=plot_info['color'], markerfmt='o', basefmt=" ")

                plt.setp(stemline, linewidth = 0.7)
                plt.setp(markerline, markersize = 3)

        # Reinitialize the cursor for the new plot
        self.cursor = mplcursors.cursor(self.ax, hover=False)
        self.cursor.connect("add", lambda sel: sel.annotation.set(
            text=f'({sel.target[0]:.2f}; {sel.target[1]:.2f})',
            fontsize=8,
            fontweight='bold',
            color='black',
            backgroundcolor='grey',
            alpha=0.7
        ))

        self.canvas.draw()

class CustomToolbar(NavigationToolbar):
    updated_selected_plots = pyqtSignal()
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
        self.checkboxes = None

    def update_plot_selector(self, plots):
        """
        Update the plot selector with a list of plot names.

        :param plots: A list of plot names to be added to the plot selector.
        """
        if self.checkboxes is None:
            self.checkboxes = {}
            for plot_name in plots:
                checkbox = QCheckBox(plot_name)
                checkbox.stateChanged.connect(self.plot_selection_changed)
                self.addWidget(checkbox)
                self.checkboxes[plot_name] = checkbox
    
    def plot_selection_changed(self):
        # Emit the signal
        self.updated_selected_plots.emit()
