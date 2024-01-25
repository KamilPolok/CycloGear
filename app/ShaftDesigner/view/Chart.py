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
        
        self.axes = []                  # List to keep track of figure axes
        self.shaft_markers = []         # List to keep track of shaft markers
        self.shaft_coordinates = []     # List to keep track of shaft coordinates
        self.shaft_dimensions = []      # List to keep track of shaft dimensions

        self.shaft_attributes = {}      # List to keep track of current shaft attributes

        self.dimension_offset = 0

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

        # Set the display setting of the figure and axes
        background_color = 'white'
        self._figure.set_facecolor(background_color)
        self.ax.set_facecolor(background_color)

        # Remove axes ticks and spines and grid lines
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines[['right', 'top', 'bottom', 'left']].set_visible(False)
        self.ax.grid(False)

        self.canvas = FigureCanvasQTAgg(self._figure)

        # Set the focus policy to accept focus and then set focus to the canvas
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.setFocus()

        # Create a custom toolbar with plot selector
        self._toolbar = CustomToolbar(self.canvas, self)
        self._toolbar.updated_selected_plots.connect(self._update_plot)
        self._toolbar.show_dimensions_checkbox.stateChanged.connect(self._draw_shaft_dimensions)

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

        self._F = self._functions['F']

        # Prepare shaft coordinates - z
        self._z = {
            'z': self._functions['z'],
            'zlabel': 'Współrzędna z [mm]',
        }

        # Prepare plot data for each plot
        self._plots = {
            title: {
                'y': self._functions[key],
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
        # Set x and y axis limits
        shaft_length = self._z['z'][-1]
        
        offset = 0.1 * shaft_length
        xmin = -offset
        xmax = shaft_length + offset
        ymin = -0.25 * shaft_length
        ymax = 0.25 * shaft_length

        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)

        # Display axes arrows
        for item in self.axes:
            item.remove()
        self.axes.clear()

        arrow_x_max = shaft_length + 0.5 * offset
       
        z_axis = self.ax.annotate(
            '', xy=(0, 0), xycoords='data',
            xytext=(arrow_x_max, 0), textcoords='data',
            arrowprops=dict(arrowstyle="<-", color='#1b5e20'),
            zorder=3
        )   
        self.axes.append(z_axis)

        z_axis_label = self.ax.text(arrow_x_max, 0, 'z [mm]', ha='left', va='center', color='#1b5e20', 
                                    fontsize=8, fontweight='bold',
                                    bbox=dict(alpha=0, zorder=3))
        
        self.axes.append(z_axis_label)

    def draw_shaft_markers(self):
        """
        Draw the shaft characteristic points on the plot.

        This method adds markers and labels for significant points along the shaft,
        such as supports and eccentric positions.
        """        
        # Remove old markers
        for item in self.shaft_markers:
            item.remove()
        self.shaft_markers.clear()

        # Draw markers
        markers = self.ax.scatter(self.points, [0] * len(self.points), color='black', s=8, zorder=5)
        self.shaft_markers.append(markers)

        # Add labels for the markers
        for marker, label in zip(self.points, self.labels):
            annotation_labels = self.ax.annotate(label, (marker, 0), textcoords="offset points", xytext=(10, -15), ha='center', zorder=5)
            self.shaft_markers.append(annotation_labels)

        self._draw_shaft_coordinates()

        self.canvas.draw()

        # Remove any active plots so they can be properly redrawn
        for plot_name in list(self.active_plots.keys()):
            for line in self.active_plots[plot_name]:
                line.remove()
            del self.active_plots[plot_name]

        self._update_plot()

    def _draw_shaft_coordinates(self):
        # Remove old coordinates
        for item in self.shaft_coordinates:
            item.remove()
        self.shaft_coordinates.clear()

        if self._toolbar.show_dimensions_checkbox.isChecked():
            # Define characteristic shaft coordinates

            # Draw dimension lines between points
            dimensions_color = 'SkyBlue'
            for i in range(len(self.points) - 1):
                start, end = self.points[i], self.points[i + 1]
                mid_point = (start + end) / 2
                distance = "{:.1f}".format(end - start)
                y_position = -self.dimension_offset

                dimension = self._draw_dimension(distance, start, end, mid_point, y_position, y_position, y_position)

                self.shaft_coordinates.extend(dimension)
        
        self.canvas.draw()
    
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
                for element in self.active_plots[plot_name]:
                    element.remove()
                del self.active_plots[plot_name]

        # Add new selected plots
        for plot_name in selected_plots:
            if plot_name not in self.active_plots:
                plot_info = self._plots[plot_name]
                plot_elements = []
                plot_line, = self.ax.plot(self._z['z'], plot_info['y'], linewidth = 1, color=plot_info['color'])
                plot_elements.append(plot_line)
                if not plot_name.lower().startswith('d'):
                    filling = self.ax.fill_between(self._z['z'], plot_info['y'], alpha=0.3, color=plot_info['color'])
                    plot_elements.append(filling)
                self.active_plots[plot_name] = plot_elements
        
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
        self.shaft_attributes = shaft_subsections_drawing_attributes

        # Remove old sections
        for section in list(self.active_sections.keys()):
            self.active_sections[section].remove()
            del self.active_sections[section]

        # Draw new sections
        for section_name, section in self.shaft_attributes.items():
            for subsection_number, subsection in section.items():
                start = subsection[0]
                length = subsection[1]
                diameter = subsection[2]

                subsection_id = f"{section_name}_{subsection_number}"

                subsection_plot = Rectangle(start, length, diameter, color='grey', linewidth=2, fill=False)
                self.active_sections[subsection_id] = subsection_plot
                self.ax.add_patch(subsection_plot)
        
        # Draw shaft dimensions
        self._draw_shaft_dimensions()

        self.canvas.draw()
    
    def _draw_shaft_dimensions(self):
        # Remove old dimenions
        for item in self.shaft_dimensions:
            item.remove()
        self.shaft_dimensions.clear()
        
        highest_diameter = 0

        if self.shaft_attributes and self._toolbar.show_dimensions_checkbox.isChecked():
            # Get the highest diameter of shaft
            for section_name, section in self.shaft_attributes.items():
                for subsection_number, subsection in section.items():
                        if subsection[-1] > highest_diameter:
                            highest_diameter = subsection[-1]

            self.dimension_offset = ((0.5 * highest_diameter ) * 1.2 + 5)

            # Draw new dimensions
            for section_name, section in self.shaft_attributes.items():
                for subsection_number, subsection in section.items():

                    # Draw length dimension
                    start = subsection[0]
                    length = subsection[1]
                    diameter = subsection[2]

                    start_z = start[0]
                    end_z = start[0] + length
                    y_position = self.dimension_offset
                    label_position = start_z + length * 0.5
                    text = "{:.1f}".format(length)

                    length_dimension = self._draw_dimension(text, start_z, end_z, label_position, y_position, y_position, y_position)
                    self.shaft_dimensions.extend(length_dimension)

                    # Draw diameter dimension
                    start_y = start[1]
                    end_y = start[1] + diameter
                    z_position = start_z + length * 0.75
                    y_position = start_y + diameter * 0.5
                    text = "Ø {:.1f}".format(diameter)

                    diameter_dimension = self._draw_dimension(text, z_position, z_position, z_position, start_y, end_y, y_position)
                    self.shaft_dimensions.extend(diameter_dimension)
        
        self._draw_shaft_coordinates()

        self.canvas.draw()

    def _draw_dimension(self, text, start_z, end_z, label_z_position, start_y=0, end_y=0, label_y_position=0):
        lines = []
        # Set dimensions color
        dimensions_color = '#c62828'

        # Draw dimension line
        dimension_line = self.ax.annotate(
            '', xy=(start_z, start_y), xycoords='data',
            xytext=(end_z, end_y), textcoords='data',
            arrowprops=dict(arrowstyle="<->", color=dimensions_color),
            zorder=3
        )
        lines.append(dimension_line)

        # Perfrom actions depending of dimension line orientation
        offset = 0.3
        if start_z == end_z:                # Vertical line
            ha, va = 'right', 'center'
            rotation = 90
            label_z_position -= offset            
        else:                               # Horizontal line
            ha, va = 'center', 'bottom'
            rotation = 0
            label_y_position += offset

            # draw reference lines for horizontal dimension lines
            for position in [start_z, end_z]:
                reference_line = self.ax.plot([position, position], [0, end_y], linestyle='-', color=dimensions_color, linewidth=0.5, zorder=0)
                lines.append(reference_line[0])

        # Add dimension labels
        dimension_label = self.ax.text(label_z_position, label_y_position, text, rotation=rotation, ha=ha, va=va, color=dimensions_color,
                                        fontsize=8,
                                        bbox=dict(alpha=0, zorder=3))
        lines.append(dimension_label)
        
        return lines

    def init_plots(self, functions, coordinates):
        """
        Create and store plot data from the provided data dictionary.

        :param data: A dictionary containing the data for the plots.
        """
        self._functions = functions
        
        shaft_points = [(0,0)] + coordinates
        self.labels = [coord[0] for coord in shaft_points]
        self.points = [coord[1] for coord in shaft_points]

        self._set_plots_data()
        self._set_axes_limits()
        self.draw_shaft_markers()

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

        # prepare checkbox for display dimensions
        self.show_dimensions_checkbox = QCheckBox('Wyświetl wymiary')
        self.addWidget(self.show_dimensions_checkbox)

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
