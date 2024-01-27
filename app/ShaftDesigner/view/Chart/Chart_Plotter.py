import mplcursors
class Chart_Plotter():
    def __init__(self, ax, canvas, toolbar):
        self._ax = ax
        self._canvas = canvas
        self._toolbar = toolbar
        self._toolbar.plots_selector.stateChanged.connect(self._refresh_selected_plots)

        # Create and store the cursor object for interactive data display
        self._cursor = mplcursors.cursor(self._ax, hover=False)

        self._plots = {}            # Dictionary to keep track of plots
        self._active_plots = {}     # Dictionary to keep track of active plots

    def _add_plot_functions(self, functions):
        """
        Prepare and set the data for each plot based on the input data.

        This method appends plots to the toolbar selector 
        """
        for key, function in functions.items():
            if key not in self._plots:
                self._toolbar.add_plot(key, function[0])
            self._plots[key] = function
            
    def _reset_plots(self):
        # Remove any active plots so they can be properly redrawn
        for plot_name in list(self._active_plots.keys()):
            for line in self._active_plots[plot_name]:
                line.remove()
            del self._active_plots[plot_name]

        self._refresh_selected_plots()

    def _refresh_selected_plots(self):
        """
        Switch the current plots based on the selected plots.
        """
        # Determine which plots are selected
        selected_plots = [plot[0] for plot in self._toolbar.plots_selector.currentOptions()]

        # Remove plots that are not selected
        for plot_name in list(self._active_plots.keys()):
            if plot_name not in selected_plots:
                for element in self._active_plots[plot_name]:
                    element.remove()
                del self._active_plots[plot_name]

        # Add new selected plots
        for plot_name in selected_plots:
            if plot_name not in self._active_plots:
                y = self._plots[plot_name][len(self._plots[plot_name]) - 1]
                color = self._plots[plot_name][2]
                plot_elements = []
                plot_line, = self._ax.plot(self._z, y, linewidth = 1, color=color)
                plot_elements.append(plot_line)
                if not plot_name.lower().startswith('d'):
                    filling = self._ax.fill_between(self._z, y, alpha=0.3, color=color)
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

    def init_plots(self, z, functions):
        """
        Create and store plot data from the provided data dictionary.

        :param z: Numpy array containing the z arguments
        :param functions: Dictionary containing the functions arrays for the plots.
        """
        self._z = z

        self._add_plot_functions(functions)
        self._reset_plots()
