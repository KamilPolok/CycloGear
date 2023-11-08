from ast import literal_eval

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QSplitter, QPushButton
from PyQt6.QtCore import Qt

MAIN_WINDOW_W = 300
MAIN_WINDOW_H = 100

class MainWindow(QMainWindow):
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
        self.materialAcqComponentLayout = QVBoxLayout()
        self.SelectMaterialBtn = QPushButton("Materiał:")
        self.materialAcqComponentLayout.addWidget(self.SelectMaterialBtn)

        self.leftSectionLayout.addLayout(self.materialAcqComponentLayout)
    

    def updateViewedMaterial(self, itemData):
        for attribute, value in itemData.items():
            layout = QHBoxLayout()
            layout.addWidget(QLabel(f"{attribute}: "))
            layout.addWidget(QLabel(f"{value[0]} "))
            layout.addWidget(QLabel(f"{value[1]}"))

            self.materialAcqComponentLayout.addLayout(layout)

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
