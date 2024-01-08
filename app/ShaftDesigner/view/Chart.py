import mplcursors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Rectangle

from PyQt6.QtWidgets import QCheckBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

class Chart(QWidget):
    """
    A class representing a chart widget in a PyQt application.

    This class is responsible for creating and managing the chart display,
    including the plot selection and updating the plot display.
    """
     
    def __init__(self, parent=None):
        super(Chart, self).__init__(parent)

        self.active_plots = {}          # Dictionary to keep track of active plots
        self.active_sections = {}       # Dictionary to keep track of shaft sections

        self.markers_and_labels = []  # List to keep track of markers and labels

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
        self._figure, self.ax = plt.subplots(constrained_layout=True)
        self.canvas = FigureCanvasQTAgg(self._figure)

        # Set the focus policy to accept focus and then set focus to the canvas
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.setFocus()

        # Create a custom toolbar with plot selector
        self._toolbar = CustomToolbar(self.canvas, self)
        self._toolbar.updated_selected_plots.connect(self._update_plot)

        # Create and store the cursor object for interactive data display
        self.cursor = mplcursors.cursor(self.ax, hover=False)

        # Add the toolbar and canvas to the layout
        layout.addWidget(self._toolbar)
        layout.addWidget(self.canvas)
    
    def _set_plots_data(self):
        """
        Prepare and set the data for each plot based on the input data.

        This method organizes the data for each plot type, including the y-values,
        plot titles, y-axis labels, and colors.
        """
        # Define plot details in a structured way
        plot_details = {
            'Mg': ('Mg(z)', 'Moment gnący Mg [Nm]', 'blue'),
            'Ms': ('Ms(z)', 'Moment skręcający Ms [Nm]', 'green'),
            'Mz': ('Mz(z)', 'Moment zastępczy Mz [Nm]', 'orange'),
            'dMz': ('d(Mz)', 'Średnica minimalna ze względu na moment zastępczy dMz [mm]', 'purple'),
            'dMs': ('d(Ms)', 'Średnica minimalna ze względu na moment skręcający dMs [mm]', 'red'),
            'dqdop': ('d(q\')', 'Średnica minimalna ze względu na dopuszczalny kąt skręcenia dq\' [mm]', 'black')
        }

        self._F = self._data['F']

        # Prepare shaft coordinates - z
        self._z = {
            'z': self._data['z'],
            'zlabel': 'Współrzędna z [mm]',
        }

        # Prepare plot data for each plot
        self._plots = {
            title: {
                'y': self._data[key],
                'title': title,
                'ylabel': ylabel,
                'color': color
            }
            for key, (title, ylabel, color) in plot_details.items()
        }

        # Update the plot selector in the toolbar
        self._toolbar.update_plot_selector([plot['title'] for plot in self._plots.values()])
        
    def _set_axes_limits(self):
        """
        Set the axes limits for the plot based on the data.

        This method calculates the overall maximum and minimum values across all plots
        and sets the x and y axis limits accordingly.
        """
        # Initialize variables to store the overall max and min values
        self.overall_max = float('-inf')
        self.overall_min = float('inf')

        for plot in self._plots.values():
            current_max = max(plot['y'])
            current_min = min(plot['y'])

            if current_max > self.overall_max:
                self.overall_max = current_max
            if current_min < self.overall_min:
                self.overall_min = current_min

        # Set z and y axis limits
        offset = 0.1 * self._data['L']
        self.ax.set_xlim([0 - offset, self._data['L'] + offset])
        self.ax.set_ylim(self.overall_min + 0.2 * self.overall_min, self.overall_max + 0.2 * self.overall_max)
        self.ax.set_xlabel(self._z['zlabel'])
        self.ax.grid(True, which='major', linestyle='-', linewidth='0.2', color='gray')
        self.ax.grid(True, which='minor', linestyle=':', linewidth='0.2', color='gray')
        self.ax.minorticks_on()

    def _draw_shaft_coordinates(self):
        """
        Draw the shaft characteristic points on the plot.

        This method adds markers and labels for significant points along the shaft,
        such as supports and eccentric positions.
        """
        roller_support = self._data['LA']
        pin_support = self._data['LB']
        eccentric1_position = self._data['L1']
        eccentric2_position = self._data['L2']
        shaft_length = self._data['L']


        # Remove old markers and labels
        for item in self.markers_and_labels:
            item.remove()
        self.markers_and_labels.clear()

        # Define markers and corresponding labels
        points = [ 0, roller_support, eccentric1_position, eccentric2_position, pin_support, shaft_length]
        labels = ['0', 'A', 'L1', 'L2', 'B', 'L']

        # Draw markers
        markers = self.ax.scatter(points, [0] * len(points), color='black', s=8, zorder=5)
        self.markers_and_labels.append(markers)

        # Add labels for the markers
        for marker, label in zip(points, labels):
            annotation_labels = self.ax.annotate(label, (marker, 0), textcoords="offset points", xytext=(10, -15), ha='center', zorder=5)
            self.markers_and_labels.append(annotation_labels)

        # Draw dimension lines between points
        dimensions_color = 'SkyBlue'
        for i in range(len(points) - 1):
            start, end = points[i], points[i + 1]
            mid_point = (start + end) / 2
            distance = end - start

            # Draw dimension line with arrows
            dimension_lines = self.ax.annotate(
                '', xy=(start, 0), xycoords='data',
                xytext=(end, 0), textcoords='data',
                arrowprops=dict(arrowstyle="<->", color=dimensions_color),
                zorder=3
            )
            self.markers_and_labels.append(dimension_lines)

            # Add dimension labels
            dimension_labels = self.ax.text(mid_point, 0, f' {distance} ', ha='center', va='center', color=dimensions_color,
                     fontsize=8,
                     bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2', zorder=3))

            self.markers_and_labels.append(dimension_labels)

        # Remove any active plots so they can be properly redrawn
        for plot_name in list(self.active_plots.keys()):
            for line in self.active_plots[plot_name]:
                line.remove()
            del self.active_plots[plot_name]

        self._update_plot()
    
    def _update_plot(self):
        """
        Switch the current plot based on the selected plot in the toolbar.

        :param selected_plot: The name of the plot to be displayed.
        """
        # Determine which plots are selected
        selected_plots = [key for key, checkbox in self._toolbar.checkboxes.items() if checkbox.isChecked()]

        # Remove plots that are not selected
        for plot_name in list(self.active_plots.keys()):
            if plot_name not in selected_plots:
                for line in self.active_plots[plot_name]:
                    line.remove()
                del self.active_plots[plot_name]

        # Add new selected plots
        for plot_name in selected_plots:
            if plot_name not in self.active_plots:
                plot_info = self._plots[plot_name]
                if plot_name.lower().startswith('d'):
                    plot_lines = self.ax.plot(self._z['z'], plot_info['y'], linewidth = 1, color=plot_info['color'])
                else:
                    markerline, stemline, baseline = self.ax.stem(self._z['z'], plot_info['y'], linefmt=plot_info['color'], markerfmt='o', basefmt=" ")
                    plt.setp(stemline, linewidth = 0.5)
                    plt.setp(markerline, markersize = 1)
                    plot_lines = [markerline, stemline, baseline]
                self.active_plots[plot_name] = plot_lines
        
        # Manage the cursor
        self._manage_cursor()

        self.canvas.draw()

    def _manage_cursor(self):
        """
        Manage the mplcursors cursor for interactive data display.
        """
        # Remove the previous cursor if it exists
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.remove()

        # Collect all current plot lines
        current_lines = [line for lines in self.active_plots.values() for line in lines if hasattr(line, 'get_xdata')]

        # Create a new cursor if there are plots
        if current_lines:
            self.cursor = mplcursors.cursor(current_lines, hover=False)
            self.cursor.connect("add", lambda sel: sel.annotation.set(
                text=f'({sel.target[0]:.2f}; {sel.target[1]:.2f})',
                fontsize=8,
                fontweight='bold',
                color='black',
                backgroundcolor='grey',
                alpha=0.7
            ))

    def draw_shaft(self, shaft_subsections_drawing_attributes):
        # Remove existing sections
        for section in list(self.active_sections.keys()):
            self.active_sections[section].remove()
            del self.active_sections[section]

        # Draw new sections
        for section_name, section in shaft_subsections_drawing_attributes.items():
            for subsection_number, subsection in section.items():
                subsection_plot = Rectangle(subsection[0], subsection[1], subsection[2], color='grey', linewidth=2, fill=False)
                self.active_sections[f"{section_name}_{subsection_number}"] = subsection_plot
                self.ax.add_patch(subsection_plot)

        self.canvas.draw()

    def init_plots(self, data):
        """
        Create and store plot data from the provided data dictionary.

        :param data: A dictionary containing the data for the plots.
        """

        self._data = data

        self._set_plots_data()
        self._set_axes_limits()
        self._draw_shaft_coordinates()

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
