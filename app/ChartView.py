import mplcursors

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class Chart(QWidget):
    def __init__(self):
        super().__init__()

        # Init UI
        self.initUI()

        # Set the focus policy to accept focus and then set focus
        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.setFocus()

    def initUI(self):
        # Set layout 
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Set plot selector
        # Set canvas, figure and axes
        self.figure, self.ax = plt.subplots(constrained_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        # Set toolbar
        self.toolbar = CustomToolbar(self.canvas, self)
        self.toolbar.activePlotSelector.currentTextChanged.connect(self.switchPlot)
        # Create and store the cursor object
        self.cursor = mplcursors.cursor(self.ax, hover=False)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def createPlots(self, data):
        self._z = data['z']

        self._y = {'Mg': [data['Mg'], 'Mg(z)', 'Moment gnący Mg [Nm]'],
                   'Ms': [data['Ms'], 'Ms(z)', 'Moment skręcający Ms [Nm]'],
                   'Mz': [data['Mz'], 'Mz(z)', 'Moment zastępczy Mz[Nm]'],
                   'd':  [data['d'], 'd(z)', 'Średnica d [mm]']
                   }
        
        self._F = data['F']
        
        self.plots = {}
        for key, value in self._y.items():
           self.plots[value[1]] = {
                "x": self._z,
                "y": value[0],
                "title": value[1],
                "xlabel": "Współrzędna z [mm]",
                "ylabel": value[2]
            }

        self.toolbar.activePlotSelector.currentTextChanged.disconnect()
        self.toolbar.updatePlotSelector([plot[1] for plot in self._y.values()])
        self.switchPlot(self.toolbar.activePlotSelector.currentText())
        self.toolbar.activePlotSelector.currentTextChanged.connect(self.switchPlot)
    
    def switchPlot(self, selectedPlot):
        self.cursor.remove()
        plot_info = self.plots[selectedPlot]
        self.ax.clear()
        self.ax.plot(plot_info["x"], plot_info["y"], color='royalblue')
        self.ax.set_title(plot_info["title"], pad=7)
        self.ax.set_xlabel(plot_info["xlabel"])
        self.ax.set_ylabel(plot_info["ylabel"])
        self.ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='black')
        self.ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='gray')
        self.ax.minorticks_on()
        self.ax.autoscale_view()
        self.ax.set_xlim([0, self._z[-1]])

        self.cursor = mplcursors.cursor(self.ax, hover=False)
        self.cursor.connect("add", lambda sel: sel.annotation.set(
            text=f'({sel.target[0]:.2f}; {sel.target[1]:.2f})',
            fontsize=8,
            fontweight='bold',
            color="black",
            backgroundcolor="cornflowerblue",
            alpha=0.7
        ))
        self.canvas.draw()

class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas,  parent=None, coordinates=False):
        super(CustomToolbar, self).__init__(canvas, parent, coordinates)
        self.activePlotSelector = QComboBox()
        self.addWidget(self.activePlotSelector)
 
    def updatePlotSelector(self, plots):
        self.activePlotSelector.clear()
        for plot in plots:
            self.activePlotSelector.addItem(plot)
