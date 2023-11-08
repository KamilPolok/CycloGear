from ast import literal_eval
from functools import partial

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QSplitter, QPushButton, QTabWidget

from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression, pyqtSignal

MAIN_WINDOW_W = 300
MAIN_WINDOW_H = 100

class MainWindow(QMainWindow):
    updatedShaftDataSignal = pyqtSignal()
    updatedSupportBearingsSignal = pyqtSignal(dict)
    updatedCycloBearingsSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        # Init Window Attributes
        self.setWindowTitle("Mechkonstruktor 2.0")
        self.setBaseSize(MAIN_WINDOW_W, MAIN_WINDOW_H)

        self.signals = [self.updatedShaftDataSignal, self.updatedSupportBearingsSignal, self.updatedCycloBearingsSignal]

        self.initUI()
    
    def initUI(self):
        # Create tab widget
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        # Create tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tabs.addTab(self.tab3, "Tab 3")
        # Initially Enable only first tab - disable 2 and 3
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        # Set list storing data and LineEdits needed in each tabs
        self.tabData = [None, None, None]
        self.tabLE = [None, None, None]
    
    def setData(self, data):
        # Set data needed for or from GUI
        self._data = data

    def onChange(self):
        pass

    # def _connectSignalsAndSlots(self):
    #     self.tabs.currentChanged.connect(self.onChange)
    
    def updateData(self):
        # Get the index of current tab
        currentTabIndex = self.tabs.currentIndex()
        # Update the tabData for current tab
        for attribute, lineEdit in self.tabLE[currentTabIndex].items():
            text = lineEdit.text()
            value = literal_eval(text) if text else None
            self.tabData[currentTabIndex][attribute][0] = value
        # Check if every attribute in current tabs tabData is not None
        # isEveryAttributeProvided = all(value[0] is not None for value in self.tabData[currentTabIndex].values())

        isEveryAttributeProvided = True
        if isEveryAttributeProvided:
            # If every attribute has been provided, complete with them the _data
            for key, value in self.tabData[currentTabIndex].items():
                if key in self._data:
                    self._data[key] = value
            # ...and enable next tab
            if currentTabIndex < self.tabs.count() - 1:
                self.tabs.setTabEnabled(currentTabIndex + 1, True)

            self.signals[currentTabIndex].emit()
        else:
            # ...else, disable all tabs that come after the current tab 
            for i in range(currentTabIndex + 1, self.tabs.count()):
                self.tabs.setTabEnabled(i, False)
    
    def setupTab1(self):
        # Set tab1 layout
        self.tab1Layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1Layout)
        # Set dict of data that are needed in this tab:
        attributesToExtract = ['L', 'L1', 'L2', 'LA', 'LB', 'Materiał', 'xz']
        self.tabData[0] = {key: self._data[key] for key in attributesToExtract}
        # Set dict of line edits
        self.tabLE[0] = {}
        # View components for input shaft attributes acquisition
        self.viewComponent1()
        self.viewComponent2()
        self.viewComponent3()
        # Set update data button
        self.updateDataBtn = QPushButton("Aktualizuj dane")
        self.tab1Layout.addWidget(self.updateDataBtn)
        self.updateDataBtn.clicked.connect(self.updateData)

    def setupTab2(self):
        # Set tab2 layout
        self.tab2Layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2Layout)
        # Set dict of data that are needed in this tab:
        attributesToExtract = ['Lh1', 'fd1', 'ft1', 'Łożyska1']
        self.tabData[1] = {key: self._data[key] for key in attributesToExtract}
        # Set dict of line edits in tab1
        self.tabLE[1] = {}
            
    def viewComponent1(self):
        component1Layout = QVBoxLayout()
        componentLabel = QLabel("Wymiary:")

        shaftLength = self.createDataInputRow('L','Długość wału', 'L')

        supportCoordinatesLabel = QLabel("Współrzędne podpór:")
        pinSupport = self.createDataInputRow('LA', 'Podpora stała A', 'L<sub>A</sub>')
        rollerSupport = self.createDataInputRow('LB','Podpora przesuwna B', 'L<sub>B</sub>')

        cycloDiscCoordinatesLabel = QLabel("Współrzędne tarcz obiegowych:")
        cycloDisc1 = self.createDataInputRow('L1', 'Tarcza obiegowa 1', 'L<sub>1</sub>')
        cycloDisc2 = self.createDataInputRow('L2','Tarcza obiegowa 2', 'L<sub>2</sub>')
   
        component1Layout.addWidget(componentLabel) 
        component1Layout.addLayout(shaftLength)
        component1Layout.addWidget(supportCoordinatesLabel)
        component1Layout.addLayout(pinSupport)
        component1Layout.addLayout(rollerSupport)
        component1Layout.addWidget(cycloDiscCoordinatesLabel)
        component1Layout.addLayout(cycloDisc1)
        component1Layout.addLayout(cycloDisc2)

        self.tab1Layout.addLayout(component1Layout)

    def viewComponent2(self):
        component2Layout = QVBoxLayout()
        componentLabel = QLabel("Współczynnik bezpieczeństwa:")
        fos = self.createDataInputRow('xz', "", "x<sub>z</sub> = ")

        component2Layout.addWidget(componentLabel)
        component2Layout.addLayout(fos)

        self.tab1Layout.addLayout(component2Layout)

    def viewComponent3(self):
        self.component2Layout = QVBoxLayout()
        componentLabel = QLabel("Materiał")
        
        self.SelectMaterialBtn = QPushButton("Wybierz Materiał")

        self.component2Layout.addWidget(componentLabel)
        self.component2Layout.addWidget(self.SelectMaterialBtn)

        self.tab1Layout.addLayout(self.component2Layout)
    
    def updateViewedMaterial(self, itemData):
        self.SelectMaterialBtn.setText(itemData['Materiał'][0])
        self.tabData[self.tabs.currentIndex()]['Materiał']  = itemData

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
        # Set input validation for LineEdit
        regex = QRegularExpression("[1-9]+")
        inputValidator = QRegularExpressionValidator(regex, lineEdit)
        lineEdit.setValidator(inputValidator)
        self.tabLE[self.tabs.currentIndex()][parameter] = lineEdit
        if self.tabData[self.tabs.currentIndex()][parameter][0] is not None:
            lineEdit.setText(f'{self.tabData[self.tabs.currentIndex()][parameter][0]}')
        # Create units label
        unitsLabel = QLabel(self.tabData[self.tabs.currentIndex()][parameter][-1])

        layout.addWidget(Descriptionlabel)
        layout.addWidget(SymbolLabel)
        layout.addWidget(lineEdit)
        layout.addWidget(unitsLabel)

        return layout
