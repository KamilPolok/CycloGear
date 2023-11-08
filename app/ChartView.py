import mplcursors

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox

class Chart(QDialog):
    def __init__(self, z, F, Mg, Ms, Mz, d):
        self._points = ['A', 'T1', 'T2', 'B']
        self._z = z
        self._y = {'Mg': [Mg, 'Mg(z)', 'Moment gnący Mg [Nm]'],
                   'Ms': [Ms, 'Ms(z)', 'Moment skręcający Ms [Nm]'],
                   'Mz': [Mz, 'Mz(z)', 'Moment zastępczy Mz[Nm]'],
                   'd':  [d, 'd(z)', 'Średnica d [mm]']
                   }
        self._F = F
        super().__init__()

        # Set active plot
        self.activePlot = self._y['d']

        self.initUI()
        self.plot()

    def initUI(self):
        # Set Window Parameters
        self.resize(800,400)
        # Set layout 
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Set plot selector
        self.activePlotSelector = QComboBox()
        for key, value in self._y.items():
            self.activePlotSelector.addItem(value[1])
        self.activePlotSelector.setCurrentText(self.activePlot[1])
        self.activePlotSelector.currentTextChanged.connect(self.switchPlot)
        # Set canvas, figure and axes
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.figure)
        # Set toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.activePlotSelector)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        mplcursors.cursor(self.ax, hover=True)

    def plot(self):
        self.ax.cla()
        
        self.ax.plot(self._z, self.activePlot[0], color='darkorange')
        self.ax
        self.ax.set_title(self.activePlot[1], pad=15)
        self.ax.set_xlabel("Współrzędna z [mm]")
        self.ax.set_ylabel(self.activePlot[2])

        self.ax.grid(True)
        self.ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='black')  # Major gridlines
        self.ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='gray')   # Minor gridlines
        self.ax.minorticks_on()  # Enable minor ticks
        self.ax.autoscale_view()
        self.ax.set_xlim([0, self._z[-1]])

        # Plot points on the x-axis

        self.ax.scatter(self._z[1:-1], self.activePlot[0][1:-1], color='red', s=25, zorder=5)  # s is the size of the points

        for label, z, y  in zip(self._points, self._z[1:-1], self.activePlot[0][1:-1]):
            self.ax.annotate(f"{label }({z},{y:.2f})", (z, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, weight='bold', color='red')

        self.canvas.draw()
    
    def switchPlot(self, selectedPlot):
        if selectedPlot is not self.activePlot[1]:
            for key, plot in self._y.items():
                if plot[1] == selectedPlot:
                    self.activePlot = plot

            print(self.activePlot)
            self.plot()
