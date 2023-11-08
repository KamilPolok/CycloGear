import sys
import numpy as np
import mplcursors
from ast import literal_eval

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QVBoxLayout, QComboBox, QLabel, QWidget, QHBoxLayout, QLineEdit, QSplitter, QPushButton
from PyQt6.QtCore import Qt

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

MAIN_WINDOW_W = 300
MAIN_WINDOW_H = 100

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        # Init Window Attributes
        self.setWindowTitle("Mechkonstruktor 2.0")
        self.setBaseSize(MAIN_WINDOW_W, MAIN_WINDOW_H)
        # Init UI
        self.initUI()
        # View section for data acquisition from user

    def initUI(self):
        # Create central widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        # Create main layout for the central widget
        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)
        # Create splitter and add it to main layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        mainLayout.addWidget(splitter)
        # Create the left and right widgets
        leftSectionWidget = QWidget(self)
        rightSectionWidget = QWidget(self)
        # Create QVBoxLayouts for the left and right widgets
        self.leftSectionLayout = QVBoxLayout()
        self.rightSectionLayout = QVBoxLayout()

        leftSectionWidget.setLayout(self.leftSectionLayout)
        rightSectionWidget.setLayout(self.rightSectionLayout)
        # Add the left and right widgets to the splitter
        splitter.addWidget(leftSectionWidget)
        splitter.addWidget(rightSectionWidget)
    
    def setData(self, data):
        self._data = data
        self._LE = {}

    def getData(self):
        for key, value in self._LE.items():
            self._data[key][0] = literal_eval(value.text()) if value.text() else 0
        
        return self._data

    def viewDataAcqSection(self):
        # Set section label
        sectionLabel = QLabel("DANE WEJŚCIOWE")
        self.leftSectionLayout.addWidget(sectionLabel)

        # View component for shaft parameters acquisition
        self.viewShaftParamsAcqComponent()
        self.viewFOSAcqComponent()
        self.viewMaterialAcqComponent()

        self.updateDataBtn = QPushButton("Aktualizuj dane")
        self.leftSectionLayout.addWidget(self.updateDataBtn)

    def viewDataDispSection(self, data):

        self.viewLoadDataComponent()
        self.viewChartBtn = QPushButton("Pokaż wykresy")
        self.rightSectionLayout.addWidget(self.viewChartBtn)

    def viewShaftParamsAcqComponent(self):
        componentLayout = QVBoxLayout()
        componentLabel = QLabel("Wymiary:")

        shaftLength = self.createDataInputRow('L','Długość wału', 'L')

        supportCoordinatesLabel = QLabel("Współrzędne podpór:")
        pinSupport = self.createDataInputRow('LA', 'Podpora stała A', 'L<sub>A</sub>')
        rollerSupport = self.createDataInputRow('LB','Podpora przesuwna B', 'L<sub>B</sub>')

        cycloDiscCoordinatesLabel = QLabel("Współrzędne tarcz obiegowych:")
        cycloDisc1 = self.createDataInputRow('L1', 'Tarcza obiegowa 1', 'L<sub>1</sub>')
        cycloDisc2 = self.createDataInputRow('L2','Tarcza obiegowa 2', 'L<sub>2</sub>')
   

        componentLayout.addWidget(componentLabel) 
        componentLayout.addLayout(shaftLength)
        componentLayout.addWidget(supportCoordinatesLabel)
        componentLayout.addLayout(pinSupport)
        componentLayout.addLayout(rollerSupport)
        componentLayout.addWidget(cycloDiscCoordinatesLabel)
        componentLayout.addLayout(cycloDisc1)
        componentLayout.addLayout(cycloDisc2)

        self.leftSectionLayout.addLayout(componentLayout)

    def viewFOSAcqComponent(self):
        componentLayout = QVBoxLayout()
        componentLabel = QLabel("Współczynnik bezpieczeństwa:")
        fos = self.createDataInputRow('xz', "", "x<sub>z</sub> = ")

        componentLayout.addWidget(componentLabel)
        componentLayout.addLayout(fos)

        self.leftSectionLayout.addLayout(componentLayout)

    def viewMaterialAcqComponent(self):
        material = {'Oznaczenie': 'Stal C45',
             'Rm': [600, 'MPa'],
             'Re': [340, 'MPa'],
             'Zgj': [460,'MPa'],
             'Zgo': [250, 'MPa'],
             'Zsj': [300, 'MPa'],
             'Zso': [150, 'MPa'],
             'E': [2100000, 'MPa'],
             'G': [80750, 'MPa'],
             'g': [7860, 'kg/m^3'],
            }
        
        componentLayout = QVBoxLayout()
        componentLabel = QLabel("Materiał:")
        materialLabel = QLabel(material['Oznaczenie'])

        componentLayout.addWidget(componentLabel)
        componentLayout.addWidget(materialLabel)

        for parameter, value in material.items():
            if parameter == 'Oznaczenie':
                continue
            layout = QHBoxLayout()
            layout.addWidget(QLabel(f"{parameter}: "))
            layout.addWidget(QLabel(f"{value[0]} "))
            layout.addWidget(QLabel(f"{value[1]}"))

            componentLayout.addLayout(layout)

        self.leftSectionLayout.addLayout(componentLayout)

    def viewLoadDataComponent(self):
        componentLayout = QVBoxLayout()
        componentLabel = QLabel("Obciążenia:")
        equalForcesLabel = QLabel("Siły wypadkowe pochodzące od tarcz:")
        f1 = self.createDataDisplayRow("F<sub>1</sub>", self._data['F1'])
        f2 = self.createDataDisplayRow("F<sub>2</sub>", self._data['F2'])
        inputTourqeLabel = QLabel("Wejściowy moment obrotowy:")
        tin = self.createDataDisplayRow("M<sub>o</sub>", self._data['Mo'])

        componentLayout.addWidget(componentLabel)
        componentLayout.addWidget(equalForcesLabel)
        componentLayout.addLayout(f1)
        componentLayout.addLayout(f2)
        componentLayout.addWidget(inputTourqeLabel)
        componentLayout.addLayout(tin)

        self.rightSectionLayout.addLayout(componentLayout)

    def createDataInputRow(self, parameter, description, symbol):
        if parameter not in self._data:
            pass
        # Set Layout of the row
        layout = QHBoxLayout()
        # Create description label
        Descriptionlabel = QLabel(description)
        # Create symbol label
        SymbolLabel = QLabel(f'{symbol} = ')
        # Create LineEdit and save it
        lineEdit = QLineEdit()
        self._LE[parameter] = lineEdit
        if self._data[parameter][0] is not None:
            lineEdit.setText(f'{self._data[parameter][0]}')
        # Create units label
        unitsLabel = QLabel(self._data[parameter][1])

        layout.addWidget(Descriptionlabel)
        layout.addWidget(SymbolLabel)
        layout.addWidget(lineEdit)
        layout.addWidget(unitsLabel)

        return layout
    
    def createDataDisplayRow(self, description, parameter):
        layout = QHBoxLayout()
        descriptionlabel = QLabel(description)
        parameterLabel = QLabel(f'{parameter[0]}')
        unitsLabel = QLabel(parameter[1])
        layout.addWidget(descriptionlabel)
        layout.addWidget(parameterLabel)
        layout.addWidget(unitsLabel)

        return layout
    
class Controller:
    def __init__(self, model, view):
        self.window = view
        self.data = model

        self.material = {'Oznaczenie': 'Stal C45',
             'Rm': [600, 'MPa'],
             'Re': [340, 'MPa'],
             'Zgj': [460,'MPa'],
             'Zgo': [250, 'MPa'],
             'Zsj': [300, 'MPa'],
             'Zso': [150, 'MPa'],
             'E': [2100000, 'MPa'],
             'G': [80750, 'MPa'],
             'g': [7860, 'kg/m^3'],
            }

        self.startup()
        self._connectSignalsAndSlots()

    def startup(self):
        # Pass necessary data to view:
        self.window.setData(self.data)
        # Init view
        self.window.viewDataAcqSection()
        self.window.viewDataDispSection(self.data)
    
    def _connectSignalsAndSlots(self):
        self.window.updateDataBtn.clicked.connect(self._performCalculations)
        self.window.viewChartBtn.clicked.connect(self.displayChart)

    def displayChart(self):
        self.chart = Chart(self.z, self.F, self.Mg, self.Ms, self.Mz, self.d)
        self.chart.exec()

    def _performCalculations(self):
        self.data = self.window.getData()
        print(self.data)
        L = self.data['L'][0]
        LA = self.data['LA'][0]
        LB = self.data['LB'][0]
        L1 = self.data['L1'][0]
        L2 = self.data['L2'][0]
        F1 = self.data['F1'][0]
        F2 = self.data['F2'][0]
        Mo = self.data['Mo'][0]
        Zgo = self.material['Zgo'][0]
        xz = self.data['xz'][0]

        self.z = [0, LA, L1, L2, LB, L]


        # Reakcje podporowe
        Rb = (-F1*L1-F2*L2)/(LB-LA)
        Ra = -F1-F2-Rb

        self.F = [0, Ra, F1, F2, Rb, 0]
        # Momenty gnące
        MgP = 0
        MgA = 0*(LA)
        Mg1 = -Ra*(L1-LA)
        Mg2 = -Ra*(L2-LA)-F1*(L2-L1)
        MgB = -Ra*(LB-LA)-F1*(LB-L1)-F2*(LB-L2)
        MgK = -Ra*(L-LA)-F1*(L-L1)-F2*(L-L2)-Rb*(L-LB)

        self.Mg = np.array([MgP, MgA, Mg1, Mg2,MgB, MgK])
        # Momenty skręcające
        self.Ms = np.array([Mo, Mo, Mo, Mo, 0, 0])
        # Momenty zastępcze
        wsp_redukcyjny = 2 * np.sqrt(3)

        self.Mz = np.sqrt(np.power(self.Mg, 2) + np.power(wsp_redukcyjny / 2 * self.Ms, 2))
        # Średnica wału
        kgo = Zgo/xz
        self.d = np.power(32*self.Mz/(np.pi*kgo*1000000), 1/3)*1000

def main():
    ## DANE
    # Wymiary, współrzędne podpór i sił
    L = 200
    LA = 80
    LB = 180
    L1 = 120
    L2 = 150

    z = [0, LA, L1, L2, LB, L]

    # Wsp bezpieczeństwa
    Xz = 3
    # Parametry materiałowe (Materiał: C45)
    Zgo = 250
    Zsj = 300
    # Wartości sił działających na wał
    W = 100     # Siła wypdakowa w mechanizmie równowodowym
    Mo = 9.55   # Moment obrotowy

    ## OBLICZENIA
    # Wartości sił pochodzących od tarcz
    F1 = W
    F2 = -W
    # Reakcje podporowe
    Rb = (-F1*L1-F2*L2)/(LB-LA)
    Ra = -F1-F2-Rb

    F = [0, Ra, F1, F2, Rb, 0]
    # Momenty gnące
    MgP = 0
    MgA = 0*(LA)
    Mg1 = -Ra*(L1-LA)
    Mg2 = -Ra*(L2-LA)-F1*(L2-L1)
    MgB = -Ra*(LB-LA)-F1*(LB-L1)-F2*(LB-L2)
    MgK = -Ra*(L-LA)-F1*(L-L1)-F2*(L-L2)-Rb*(L-LB)

    Mg = np.array([MgP, MgA, Mg1, Mg2,MgB, MgK])
    # Momenty skręcające
    Ms = np.array([Mo, Mo, Mo, Mo, 0, 0])
    # Momenty zastępcze
    wsp_redukcyjny = 2 * np.sqrt(3)

    Mz = np.sqrt(np.power(Mg, 2) + np.power(wsp_redukcyjny / 2 * Ms, 2))
    # Średnica wału
    kgo = Zgo/Xz
    d = np.power(32*Mz/(np.pi*kgo*1000000), 1/3)*1000

    # print("\n".join(map(str, [Mg, Ms, Mz, d])))
    # print(np.max(d))

    app = QApplication([])
    # chartWindow = Chart(z, F, Mg, Ms, Mz, d)
    # chartWindow.show()

    data = {
            'F1': [100, 'N'],
            'F2': [-100, 'N'],
            'Mo': [9.55, 'Nm'],
            'L': [None, 'mm'],
            'LA': [None, 'mm'],
            'LB': [None, 'mm'],
            'L1': [None, 'mm'],
            'L2': [None, 'mm'],
            'e': [10, 'mm'],
            'xz': [None, '']
            }

    view = View()
    ctrl = Controller(data, view)
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
