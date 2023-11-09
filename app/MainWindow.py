from ast import literal_eval
from functools import partial

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QSplitter, QPushButton, QTabWidget

from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression, pyqtSignal

MAIN_WINDOW_W = 300
MAIN_WINDOW_H = 100

class MainWindow(QMainWindow):
    updatedShaftDataSignal = pyqtSignal()
    updatedSupportBearingsSignal = pyqtSignal()
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
        self.tab4 = QWidget()
        
        self.tabs.addTab(self.tab1, "Założenia wstępne")
        self.tabs.addTab(self.tab2, "Łożyska podporowe")
        self.tabs.addTab(self.tab3, "Łożyska cykloidalne")
        self.tabs.addTab(self.tab4, "Wyniki obliczeń")
        # Initially Enable only first tab - disable 2 and 3
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        # Set list storing data and lineEdits needed in each tabs
        self.lineEdits = {}
        self.valueLabels = {}
        self.tabsData = [None, None, None, None]
    
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
        for attribute, values in self.tabsData[currentTabIndex].items():
            if attribute in self.lineEdits:
                text = self.lineEdits[attribute].text()
                value = literal_eval(text) if text else None
                self.tabsData[currentTabIndex][attribute][0] = value
        # Check if every attribute in current tabs tabData is not None
        # Check if in the tabsData[currentTabIndex] is any None value
        # isEveryAttributeProvided = all(value[0] is not None for value in self.tabsData[currentTabIndex].values())

        isEveryAttributeProvided = True
        if isEveryAttributeProvided:
            # If every attribute has been provided, complete with them the _data
            for key, value in self.tabsData[currentTabIndex].items():
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
        self.tabsData[0] = {key: self._data[key] for key in attributesToExtract}
        # View components of tab1
        self.viewComponent1()
        self.viewComponent2()
        self.viewComponent3()
        # Set update data button
        self.updateDataBtn = QPushButton("Aktualizuj dane")
        self.tab1Layout.addWidget(self.updateDataBtn)
        self.updateDataBtn.clicked.connect(self.updateData)

    def setupTab2(self):
        #Set tab2 layout
        self.tab2Layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2Layout)
        # Create splitter and add it to main layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.tab2Layout.addWidget(splitter)
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

        # Set dict of data that are needed in this tab:
        attributesToExtract = ['Lh1', 'fd1', 'ft1', 'Łożyska1']
        self.tabsData[1] = {key: self._data[key] for key in attributesToExtract}
        # View sections of tab2
        self.viewSection1()
        self.viewSection2()
    
    # def setupTab3(self):
    #     #Set tab3 layout
    #     self.tab3Layout = QVBoxLayout()
    #     self.tab3.setLayout(self.tab2Layout)
    #     # Create splitter and add it to main layout
    #     splitter = QSplitter(Qt.Orientation.Horizontal)
    #     self.tab3Layout.addWidget(splitter)
    #     # Create the left and right widgets
    #     leftSectionWidget = QWidget(self)
    #     rightSectionWidget = QWidget(self)
    #     # Create QVBoxLayouts for the left and right widgets
    #     self.leftSectionLayout = QVBoxLayout()
    #     self.rightSectionLayout = QVBoxLayout()

    #     leftSectionWidget.setLayout(self.leftSectionLayout)
    #     rightSectionWidget.setLayout(self.rightSectionLayout)
    #     # Add the left and right widgets to the splitter
    #     splitter.addWidget(leftSectionWidget)
    #     splitter.addWidget(rightSectionWidget)

    #     # Set dict of data that are needed in this tab:
    #     attributesToExtract = ['Lh2', 'fd2', 'ft2', 'Łożyska2']
    #     self.tabsData[2] = {key: self._data[key] for key in attributesToExtract}
    #     # View sections of tab2
    #     self.viewSection21()
    #     self.viewSection2()
        
    def viewSection1(self):
        shaftDiameter = self.createDataDisplayRow('ds','Średnica wału', 'd<sub>s</sub>')
        Lh = self.createDataInputRow('Lh1', 'trwałość godzinowa łożyska', 'f<sub>d</sub>')
        fd = self.createDataInputRow('ft1', 'współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = self.createDataInputRow('fd1', 'współczynnik zależny od temperatury pracy łozyska', 'f<sub>t</sub>')
        # Set update data button
        self.updateDataBtn = QPushButton("Aktualizuj dane")
        self.updateDataBtn.clicked.connect(self.updateData)
        # Set 
        self.SelectBearingBtn = QPushButton("Wybierz łożysko")

        self.leftSectionLayout.addLayout(shaftDiameter)
        self.leftSectionLayout.addLayout(Lh)
        self.leftSectionLayout.addLayout(fd)
        self.leftSectionLayout.addLayout(ft)
        self.leftSectionLayout.addWidget(self.updateDataBtn)
        self.leftSectionLayout.addWidget(self.SelectBearingBtn)
    
    def viewSection21(self):
        shaftDiameter = self.createDataDisplayRow('de','Średnica wału', 'd<sub>s</sub>')
        Lh = self.createDataInputRow('Lh1', 'trwałość godzinowa łożyska', 'f<sub>d</sub>')
        fd = self.createDataInputRow('ft1', 'współczynnik zależny od zmiennych obciążeń dynamicznych', 'f<sub>d</sub>')
        ft = self.createDataInputRow('fd1', 'współczynnik zależny od temperatury pracy łozyska', 'f<sub>t</sub>')
        # Set update data button
        self.updateDataBtn = QPushButton("Aktualizuj dane")
        self.updateDataBtn.clicked.connect(self.updateData)
        # Set 
        self.SelectBearingBtn2 = QPushButton("Wybierz łożysko")

        self.leftSectionLayout.addLayout(shaftDiameter)
        self.leftSectionLayout.addLayout(Lh)
        self.leftSectionLayout.addLayout(fd)
        self.leftSectionLayout.addLayout(ft)
        self.leftSectionLayout.addWidget(self.updateDataBtn)
        self.leftSectionLayout.addWidget(self.SelectBearingBtn)

    def updateViewedBearing(self, itemData):
        print(itemData)
        self.SelectBearingBtn.setText(itemData['kod'][0])
        self.tabsData[self.tabs.currentIndex()]['Łożyska1'] = itemData

    def updateViewedBearing2(self, itemData):
        print(itemData)
        self.SelectBearingBtn.setText(itemData['kod'][0])
        self.tabsData[self.tabs.currentIndex()]['Łożyska1'] = itemData
    
    
    def viewSection2(self):
        pass
    
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
        self.tabsData[self.tabs.currentIndex()]['Materiał'] = itemData

    def createDataInputRow(self, attribute, description, symbol):
        if attribute not in self._data:
            pass
        # Set Layout of the row
        layout = QHBoxLayout()
        # Create description label
        Descriptionlabel = QLabel(description)
        # Create symbol label
        SymbolLabel = QLabel(f'{symbol} = ')
        # Create LineEdit
        lineEdit = QLineEdit()
        # Fill in the Line Edit if attribute already has a value
        value = self._data[attribute][0]
        if value is not None:
            lineEdit.setText(f'{value}')
        # Set input validation for LineEdit
        regex = QRegularExpression("[0-9]+")
        inputValidator = QRegularExpressionValidator(regex, lineEdit)
        lineEdit.setValidator(inputValidator)
        # Create units label
        unitsLabel = QLabel(self._data[attribute][-1])

        layout.addWidget(Descriptionlabel)
        layout.addWidget(SymbolLabel)
        layout.addWidget(lineEdit)
        layout.addWidget(unitsLabel)
        # Save the LineEdit
        self.lineEdits[attribute] = lineEdit

        return layout

    def createDataDisplayRow(self, attribute, description, symbol):
        layout = QHBoxLayout()
        descriptionlabel = QLabel(description)
        attributeLabel = QLabel(symbol)
        valueLabel = QLabel(self._data[attribute][0] if self._data[attribute][0] is not None else '')
        unitsLabel = QLabel(attribute[1])
        layout.addWidget(descriptionlabel)
        layout.addWidget(attributeLabel)
        layout.addWidget(valueLabel)
        layout.addWidget(unitsLabel)

        self.valueLabels[attribute] = valueLabel

        return layout
