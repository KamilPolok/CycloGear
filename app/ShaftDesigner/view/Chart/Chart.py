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

        self._axes_arrows = []  # List to keep track of figure axes

        # Adjust subplot parameters to make the plot fill the figure canvas
        self.figure.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)

        # Set background color
        self._set_background_color()

        # Remove axes spines, ticks and grid lines
        self._strip_canvas()

    def _set_background_color(self, color='white'):
        self.figure.set_facecolor(color)
        self.axes.set_facecolor(color)

    def _strip_canvas(self):
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

    def _draw_axes_arrows(self):
        '''
        Draw axes on the canvas.
        '''
        for item in self._axes_arrows:
            item.remove()
        self._axes_arrows.clear()

        xlim = self.axes.get_xlim()
        z_axis = self.axes.annotate('', xy=(xlim[1], 0), xytext=(xlim[0], 0),
                           arrowprops=dict(arrowstyle="->", color="#1b5e20", lw=1),
                           zorder=3,
                           annotation_clip=False)
        
        self._axes_arrows.append(z_axis)

        self.figure.canvas.draw_idle()

    def set_initial_axes_limits(self, xlim, ylim):
        '''
        Save initial axes limits.

        Args:
            xlim (tuple): tuple (min, max) of x axis limits.
            ylim (tuple): tuple (min, max) of y axis limits.
        '''
        self.initial_xlim = xlim
        self.initial_ylim = ylim

        self._draw_axes_arrows()

    def reset_initial_view(self):
        '''
        Reset the plot view to its original view.
        '''
        self.axes.set_xlim(self.initial_xlim)
        self.axes.set_ylim(self.initial_ylim)
        
        self.axes.figure.canvas.draw_idle()

    def get_controls(self):
        return (self.axes, self.figure.canvas)

class Toolbar(NavigationToolbar):
    """
    A custom toolbar class for the chart widget, extending the NavigationToolbar.
    """

    def __init__(self, canvas: Chart, parent=None, coordinates=False):
        """
        Initialize the custom toolbar.

        Args:
            canvas (FigureCanvas): The canvas associated with the toolbar.
            parent (QWidget): The parent of the toolbar.
            coordinates (bool): Flag to show coordinates on the toolbar.
        """
        super(Toolbar, self).__init__(canvas, parent, coordinates)
        self._canvas = canvas

    def home(self, *args):
        '''
        Override home button - custom reset to initial view.
        '''
        self._canvas.reset_initial_view()
