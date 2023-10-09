import sys

from ast import literal_eval

from PyQt6.QtCore import (
    Qt,
    QRegularExpression,
)

from PyQt6.QtGui import QRegularExpressionValidator

from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database import DatabaseHandler

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 500

class DBDisplayController:
    def __init__(self, model, view):
        self._dbHandler = model
        self._window = view
        
        self._startup()
        self._connectSignalsAndSlots()
    
    def _startup(self):
        self._availableTables = self._dbHandler.getAvailableTables()
        self._activeTable = self._availableTables[0]
        self._dbHandler.setActiveTable(self._activeTable)

        self._limits = self._dbHandler.getFilterConditions()
        
        self._window.initUI(self._availableTables,
                            self._dbHandler.getActiveTableAttributes(),
                            self._dbHandler.getFilteredResults(self._limits)
                            )
    
    def _switchActiveTableEvent(self):
        activeTableIndex = self._window.activeTableSelector.currentIndex()

        self._activeTable = self._availableTables[activeTableIndex]
        self._dbHandler.setActiveTable(self._activeTable)

        self._limits = self._dbHandler.getFilterConditions()
        updatedResults = self._dbHandler.getFilteredResults(self._limits)
        self._window.DBDisplay.updateDBList(updatedResults)

    def _updateResultsEvent(self):
        for attribute, attributeLimits in self._limits.items():
            for limit in attributeLimits:
                text = self._window.filters[attribute].filterLineEdits[limit].text()
                number = literal_eval(text) if text else 0
                attributeLimits[limit] = number

        updatedResults = self._dbHandler.getFilteredResults(self._limits)
        self._window.DBDisplay.updateDBList(updatedResults)

    def _selectItemEvent(self, item):
        customWidget = self._window.DBDisplay.listWidget.itemWidget(item)
        if customWidget:
            item_text = "\t".join(label.text() for label in customWidget.findChildren(QLabel))
            print(f"Item clicked: {item_text}")

    def _connectSignalsAndSlots(self):
        self._window.activeTableSelector.activated.connect(self._switchActiveTableEvent)
        self._window.filterResultsButton.clicked.connect(self._updateResultsEvent)
        self._window.DBDisplay.listWidget.itemClicked.connect(self._selectItemEvent)
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BAZA ŁOŻYSK TOCZNYCH")
        self.setFixedSize(WINDOW_WIDTH,WINDOW_HEIGHT)

        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
    
    def initUI(self, availableTables, activeTableAttributes, dbDataframe):
        self._availableTables = availableTables
        self._activeTableAttributes = activeTableAttributes
        self._dbDataframe = dbDataframe
        # call this methods not from Window class, but from Controller, passing needed arguments
        self._createActiveTableSelector()
        self._createFilters()
        self._createDBDisplay()

    def _createActiveTableSelector(self):
        self.activeTableSelector = QComboBox()

        for table in self._availableTables:
             self.activeTableSelector.addItem(table)

        self.generalLayout.addWidget(self.activeTableSelector)
    def _createFilters(self):
        self.filtersLayout = QVBoxLayout()
        self.filters = {}

        for attribute in self._activeTableAttributes:
            filter = Filter(attribute)

            self.filtersLayout.addLayout(filter.filterLayout)
            self.filters[attribute] = filter

        self.filterResultsButton = QPushButton("FILTRUJ")

        self.generalLayout.addLayout(self.filtersLayout)
        self.filtersLayout.addWidget(self.filterResultsButton)

    def _createDBDisplay(self):
        self.DBDisplay = DBDisplay(self._dbDataframe)

        self.generalLayout.addWidget(self.DBDisplay)

class DBDisplay(QWidget):
    def __init__(self, dbDataframe):
        super().__init__()
        self._dbDataframe = dbDataframe

        self._createDisplay()

    def _createDisplay(self):
        self.displayLayout = QVBoxLayout()
        self.setLayout(self.displayLayout)

        self._createHeader()
        self._createDBList()
    
    def _createHeader(self):
        header = self._createRow(self._dbDataframe.columns)
        self.displayLayout.addWidget(header)

    def _createDBList(self):
        self.listWidget = QListWidget()
        self.updateDBList(self._dbDataframe)
        self.displayLayout.addWidget(self.listWidget)


    def updateDBList(self, df):
        self.listWidget.clear()
        for index, dfRow in df.astype('str').iterrows():

            customWidget = self._createRow(dfRow)

            item = QListWidgetItem()
            item.setSizeHint(customWidget.sizeHint())  
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, customWidget)

    def _createRow(self, dfRow):
        customWidget = QWidget()
        customWidget.setFixedWidth(400)
        customLayout = QHBoxLayout()

        for cellValue in dfRow:
            cellLabel = QLabel(str(cellValue))
            cellLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

            customLayout.addWidget(cellLabel)

        customWidget.setLayout(customLayout)
        
        return customWidget

class Filter(QWidget):
    def __init__(self, filterName):
        super().__init__()
        self.filterName = filterName

        self._createFilter()

    def _createFilter(self):
        self.filterLineEdits = {}
        self.filterLayout = QHBoxLayout()

        limits = ['min', 'max']

        nameLabel = QLabel(self.filterName)
        nameLabel.setFixedWidth(50)
        self.filterLayout.addWidget(nameLabel)

        for limit in limits:
            limitLayout = QHBoxLayout()

            limitLineEdit = QLineEdit()
            limitLineEdit.setFixedWidth(60)
            limitLineEdit.setMaxLength(8)
            reg_ex = QRegularExpression("[0-9]+\.?[0-9]+")
            input_validator = QRegularExpressionValidator(reg_ex, limitLineEdit)
            limitLineEdit.setValidator(input_validator)

            limitLabel = QLabel(limit)
            limitLabel.setFixedWidth(40)

            limitLayout.addWidget(limitLabel)
            limitLayout.addWidget(limitLineEdit)

            self.filterLayout.addLayout(limitLayout)

            self.filterLineEdits[limit] = limitLineEdit

def main():
    dbApp = QApplication([])
    dbHandler = DatabaseHandler()
    
    window = Window()
    window.show()

    displayController = DBDisplayController(model=dbHandler, view=window)

    sys.exit(dbApp.exec())

if __name__ == "__main__":
    main()

