from matplotlib.patches import Rectangle

from .Chart import Chart

class Chart_ShaftViewer():
    def __init__(self, chart: Chart):
        self._chart = chart
        
        self._shaft_dimensions = []           # Stores dimensions of every shaft step

        self._shaft_plot = []                 # Keeps track of shaft plot items
        self._shaft_dimensions_plot = []      # Keeps track of shaft dimensions plot items
        self._shaft_coordinates_plot = []     # Keeps track of shaft coordinates plot items
        self._shaft_markers = []              # Keeps track of shaft markers plot items

        self._dimension_offset = 0

        self._get_chart_controls()

    def _get_chart_controls(self):
        self._ax, self._canvas = self._chart.get_controls()

    def _set_axes_limits(self):
        """
        Set the axes limits for the plot based on the data.

        Get the shaft length from the points (last position) 
        and sets the axes limits.
        """
        shaft_length = self.points[-1]
        
        offset = 0.1 * shaft_length

        xlim = (-offset, shaft_length + offset)
        ylim = (-0.5 * (shaft_length + offset), 0.5 * (shaft_length + offset))

        self._ax.set_xlim(xlim)
        self._ax.set_ylim(ylim)

        self._chart.set_initial_axes_limits(xlim, ylim)
    
    def _get_dimension_offset(self):
        """
        Get the offset from the shaft that applies to shaft coordinates 
        and dimensions plots, so they get displayed neatly and do not
        overlay with shaft plot.
        """        
        highest_diameter = 0

        for step_dimensions in self._shaft_dimensions:
            step_diameter = step_dimensions['d']
            if step_diameter > highest_diameter:
                highest_diameter = step_diameter

        if highest_diameter != 0:
            self._dimension_offset = ((0.5 * highest_diameter ) * 1.2 + 5)

    def _draw_shaft_markers(self):
        """
        Draw the shaft characteristic points on the plot.

        This method adds markers and labels for significant points along the shaft,
        such as supports and eccentric positions.
        """        
        # Remove old markers
        for item in self._shaft_markers:
            item.remove()
        self._shaft_markers.clear()

        # Draw markers
        markers = self._ax.scatter(self.points, [0] * len(self.points),
                                   color=self._chart.markers_color,
                                   s=8,
                                   zorder=self._chart.markers_layer
                                   )
        self._shaft_markers.append(markers)
        
        # Draw labels for the markers
        for marker, label in zip(self.points, self.labels):
            annotation_label = self._ax.annotate(label, (marker, 0), 
                                                  textcoords="offset points",
                                                  xytext=(10, -15),
                                                  ha='center',
                                                  color=self._chart.markers_color,
                                                  zorder=self._chart.markers_layer
                                                  )
            self._shaft_markers.append(annotation_label)
            
        self._canvas.draw()

        # Redraw shaft coordinates
        if self._shaft_coordinates_plot:
            self.draw_shaft_coordinates()

    def _draw_dimension(self, text, start_z, end_z, label_z_position, start_y=0, end_y=0, label_y_position=0):
        lines = []

        # Draw dimension line
        dimension_line = self._ax.annotate('', xy=(start_z, start_y), xycoords='data',
                                           xytext=(end_z, end_y), textcoords='data',
                                           arrowprops=dict(arrowstyle="<->", color=self._chart.dimensions_color),
                                           zorder=self._chart.dimensions_layer
                                           )
        lines.append(dimension_line)

        # Perfrom actions depending of dimension line orientation
        offset = 0.3
        if start_z == end_z:                # Vertical line
            ha, va = 'right', 'center'
            rotation = 90
            label_z_position -= offset

            # if it is eccentric dimension, draw additional point marking the middle (y) of the section
            if end_y == 0:
                middle_point = self._ax.scatter(start_z, start_y,
                                   s=8,
                                   color=self._chart.dimensions_color,
                                   zorder=self._chart.dimensions_layer
                                   )
                lines.append(middle_point)            
        else:                               # Horizontal line
            ha, va = 'center', 'bottom'
            rotation = 0
            label_y_position += offset

            # draw reference lines for horizontal dimension lines
            for position in [start_z, end_z]:
                reference_line = self._ax.plot([position, position], [0, end_y], 
                                               linestyle='-',
                                               linewidth=0.5,
                                               color=self._chart.dimensions_color,
                                               zorder=self._chart.dimensions_layer
                                               )
                lines.append(reference_line[0])

        # Add dimension labels
        dimension_label = self._ax.text(label_z_position, label_y_position, text,
                                        rotation=rotation,
                                        ha=ha,
                                        va=va,
                                        fontsize=8,
                                        color=self._chart.dimensions_color,
                                        bbox=dict(alpha=0, zorder=self._chart.dimensions_layer)
                                        )
        lines.append(dimension_label)
        
        return lines

    def draw_shaft(self, shaft_dimensions):
        self._shaft_dimensions = shaft_dimensions

        # Remove old steps plots
        for step_plot in self._shaft_plot:
            step_plot.remove()
        self._shaft_plot.clear()

        # Plot new steps
        for step_dimensions in self._shaft_dimensions:
            start = step_dimensions['start']
            length = step_dimensions['l']
            diameter = step_dimensions['d']

            step_plot = Rectangle(start, length, diameter,
                                        linewidth=2,
                                        fill=False,
                                        color=self._chart.shaft_color,
                                        zorder=self._chart.shaft_layer
                                        )
            self._shaft_plot.append(step_plot)
            self._ax.add_patch(step_plot)

        self._canvas.draw()

        # Redraw shaft dimensions and coordinates
        if self._shaft_dimensions_plot:
            self.draw_shaft_dimensions()
            
        if self._shaft_coordinates_plot:
            self.draw_shaft_coordinates()

    def init_shaft(self, coordinates):
        shaft_points = [(0,0)] + coordinates
        self.labels = [coord[0] for coord in shaft_points]
        self.points = [coord[1] for coord in shaft_points]

        self._set_axes_limits()
        self._draw_shaft_markers()
    
    def draw_shaft_dimensions(self):
        # Remove old dimensions
        self.remove_shaft_dimensions()

        # Draw new dimensions
        self._get_dimension_offset()

        for step_dimensions in self._shaft_dimensions:
            # Draw length dimension
            start = step_dimensions['start']
            length = step_dimensions['l']
            diameter = step_dimensions['d']

            start_z = start[0]
            end_z = start[0] + length
            y_position = self._dimension_offset
            label_position = start_z + length * 0.5
            text = "{:.1f}".format(length)

            length_dimension = self._draw_dimension(text, start_z, end_z, label_position, y_position, y_position, y_position)
            self._shaft_dimensions_plot.extend(length_dimension)

            # Draw diameter dimension
            start_y = start[1]
            end_y = start[1] + diameter
            z_position = start_z + length * 0.75
            y_position = start_y + diameter * 0.5
            text = "Ø {:.1f}".format(diameter)

            diameter_dimension = self._draw_dimension(text, z_position, z_position, z_position, start_y, end_y, y_position)
            self._shaft_dimensions_plot.extend(diameter_dimension)

            # Draw eccentric
            if 'e' in step_dimensions:
                eccentric = step_dimensions['e']
                start_y = eccentric
                end_y = 0
                z_position = start_z + length * 0.5
                y_position = eccentric * 0.5
                text = "{:.1f}".format(abs(eccentric))
                diameter_dimension = self._draw_dimension(text, z_position, z_position, z_position, start_y, end_y, y_position)
                self._shaft_dimensions_plot.extend(diameter_dimension)

        self._canvas.draw()

    def draw_shaft_coordinates(self):
        # Remove old coordinates
        self.remove_shaft_coordinates()

        # Draw new coordinates
        self._get_dimension_offset()
        for i in range(len(self.points) - 1):
            start, end = self.points[i], self.points[i + 1]
            mid_point = (start + end) / 2
            distance = "{:.1f}".format(end - start)
            y_position = -self._dimension_offset

            dimension = self._draw_dimension(distance, start, end, mid_point, y_position, y_position, y_position)

            self._shaft_coordinates_plot.extend(dimension)
        
        self._canvas.draw()

    def remove_shaft_dimensions(self):
        # Remove dimensions
        for item in self._shaft_dimensions_plot:
            item.remove()
        self._shaft_dimensions_plot.clear()

        self._canvas.draw()

    def remove_shaft_coordinates(self):
        # Remove coordinates
        for item in self._shaft_coordinates_plot:
            item.remove()
        self._shaft_coordinates_plot.clear()

        self._canvas.draw()
