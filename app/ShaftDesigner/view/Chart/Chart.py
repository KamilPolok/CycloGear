from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

class Chart(FigureCanvas):
    """
    A class representing a chart widget in a PyQt application.

    This class is responsible for creating and managing the chart display,
    including the plot selection and updating the plot display.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)        
        self.axes = self.figure.add_subplot(111)
        super(Chart, self).__init__(self.figure)
        self.setParent(parent)

        # Set background color
        self._set_background_color()

        # Remove axes spines, ticks and grid lines
        self.strip_canvas()

    def _set_background_color(self, color='white'):
        self.figure.set_facecolor(color)
        self.axes.set_facecolor(color)

    def strip_canvas(self):
        # Remove spines
        self.axes.spines[['right', 'top', 'bottom', 'left']].set_visible(False)

        # Remove x and y tick labels
        self.axes.set_xticks([])
        self.axes.set_yticks([])

        # Remove the ticks if desired
        self.axes.xaxis.set_ticks_position('none') 
        self.axes.yaxis.set_ticks_position('none')

        # Remove grid lines
        self.axes.grid(False)

    def get_controls(self):
        return (self.axes, self.figure.canvas)

class Toolbar(NavigationToolbar):
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
        super(Toolbar, self).__init__(canvas, parent, coordinates)
