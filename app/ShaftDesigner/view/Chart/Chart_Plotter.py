import mplcursors

class Chart_Plotter():
    def __init__(self, ax, canvas, toolbar):
        self._ax = ax
        self._canvas = canvas
        self._toolbar = toolbar
        self._toolbar.updated_selected_plots.connect(self._refresh_selected_plots)

        # Create and store the cursor object for interactive data display
        self._cursor = mplcursors.cursor(self._ax, hover=False)

        self._active_plots = {}          # Dictionary to keep track of active plots

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

    def _reset_plots(self):
        # Remove any active plots so they can be properly redrawn
        for plot_name in list(self._active_plots.keys()):
            for line in self._active_plots[plot_name]:
                line.remove()
            del self._active_plots[plot_name]

        self._refresh_selected_plots()

    def _refresh_selected_plots(self):
        """
        Switch the current plot based on the selected plot in the toolbar.

        :param selected_plot: The name of the plot to be displayed.
        """
        # Determine which plots are selected
        selected_plots = [key for key, checkbox in self._toolbar.checkboxes.items() if checkbox.isChecked()]

        # Remove plots that are not selected
        for plot_name in list(self._active_plots.keys()):
            if plot_name not in selected_plots:
                for element in self._active_plots[plot_name]:
                    element.remove()
                del self._active_plots[plot_name]

        # Add new selected plots
        for plot_name in selected_plots:
            if plot_name not in self._active_plots:
                plot_info = self._plots[plot_name]
                plot_elements = []
                plot_line, = self._ax.plot(self._z['z'], plot_info['y'], linewidth = 1, color=plot_info['color'])
                plot_elements.append(plot_line)
                if not plot_name.lower().startswith('d'):
                    filling = self._ax.fill_between(self._z['z'], plot_info['y'], alpha=0.3, color=plot_info['color'])
                    plot_elements.append(filling)
                self._active_plots[plot_name] = plot_elements
        
        # Manage the cursor
        self._refresh_cursor()

        self._canvas.draw()

    def _refresh_cursor(self):
        """
        Refresh the mplcursors cursor for interactive data display.
        """
        # Remove the previous cursor if it exists
        if hasattr(self, 'cursor') and self._cursor:
            self._cursor.remove()

        # Collect all current plot lines
        current_lines = [line for lines in self._active_plots.values() for line in lines if hasattr(line, 'get_xdata')]

        # Create a new cursor if there are plots
        if current_lines:
            self._cursor = mplcursors.cursor(current_lines, hover=False)
            self._cursor.connect("add", lambda sel: sel.annotation.set(
                text=f'({sel.target[0]:.2f}; {sel.target[1]:.2f})',
                fontsize=8,
                fontweight='bold',
                color='black',
                backgroundcolor='grey',
                alpha=0.7
            ))

    def init_plots(self, functions):
        """
        Create and store plot data from the provided data dictionary.

        :param data: A dictionary containing the data for the plots.
        """
        self._functions = functions

        self._set_plots_data()
        self._reset_plots()
