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

class DBController:
    def __init__(self, model, view):
        self._dbHandler = model
        self._window = view
        
        self._startup()
        self._connectSignalsAndSlots()
    
    def _startup(self):
        #Set active table
        self._availableTables = self._dbHandler.getAvailableTables()
        self._activeTable = self._availableTables[0]
        self._dbHandler.setActiveTable(self._activeTable)
        #Init UI
        self._limits = self._dbHandler.getFilterConditions()
        self._window.viewActiveTableSelector(self._availableTables)
        self._window.viewFilters(self._dbHandler.getActiveTableAttributes())
        self._window.viewTableItems(self._dbHandler.getFilteredResults(self._limits))
    
    def _switchActiveTableEvent(self):
        #Check if selected table is not active table
        selectedTableIndex = self._window.activeTableSelector.currentIndex()
        selectedTable = self._availableTables[selectedTableIndex]

        if self._activeTable is not selectedTable:
            #Set new active table
            self._activeTable = selectedTable
            self._dbHandler.setActiveTable(self._activeTable)
            #Update limits - get them from new active table
            self._limits = self._dbHandler.getFilterConditions()
            updatedResults = self._dbHandler.getFilteredResults(self._limits)
            #Update view
            self._window.TableItemsView.updateItemsView(updatedResults)
            self._window.ItemsFiltersView.updateFiltersView(self._dbHandler.getActiveTableAttributes())

    def _updateResultsEvent(self):
        #Update limits - get them from lineEdits
        for attribute, attributeLimits in self._limits.items():
            for limit in attributeLimits:
                text = self._window.ItemsFiltersView.filtersLineEdits[attribute][limit].text()
                number = literal_eval(text) if text else 0
                attributeLimits[limit] = number
        #Update items view
        updatedResults = self._dbHandler.getFilteredResults(self._limits)
        self._window.TableItemsView.updateItemsView(updatedResults)

    def _selectItemEvent(self, item):
        #Exract the selected item attributes
        rowWidget = self._window.TableItemsView.itemsList.itemWidget(item)
        if rowWidget:
            item_text = "\t".join(label.text() for label in rowWidget.findChildren(QLabel))
            print(f"Item clicked: {item_text}")

    def _connectSignalsAndSlots(self):
        self._window.activeTableSelector.activated.connect(self._switchActiveTableEvent)
        self._window.ItemsFiltersView.filterResultsButton.clicked.connect(self._updateResultsEvent)
        self._window.TableItemsView.itemsList.itemClicked.connect(self._selectItemEvent)
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BAZA ŁOŻYSK TOCZNYCH")
        self.setFixedSize(WINDOW_WIDTH,WINDOW_HEIGHT)

        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
    
    def viewActiveTableSelector(self, availableTables):
        self.activeTableSelector = QComboBox()

        for table in availableTables:
             self.activeTableSelector.addItem(table)

        self.generalLayout.addWidget(self.activeTableSelector)
    
    def viewFilters(self, tableAttributes):
        self.ItemsFiltersView = ItemsFiltersView()
        self.ItemsFiltersView.updateFiltersView(tableAttributes)

        self.generalLayout.addWidget(self.ItemsFiltersView)

    def viewTableItems(self, tableItemsDf):
        self.TableItemsView = TableItemsView()
        self.TableItemsView.updateItemsView(tableItemsDf)

        self.generalLayout.addWidget(self.TableItemsView)

class TableItemsView(QWidget):
    def __init__(self):
        super().__init__()

        self._initView()

    def _initView(self):
        #Init layout with dummy widget and empty list widget
        self.itemsViewLayout = QVBoxLayout()
        self.setLayout(self.itemsViewLayout)

        self._itemsListHeader = QWidget()
        self.itemsList = QListWidget()

        self.itemsViewLayout.addWidget(self._itemsListHeader)
        self.itemsViewLayout.addWidget(self.itemsList)

    def updateItemsView(self, tableItemsDf):
        self._updateItemsListHeaderView(tableItemsDf)
        self._updateItemsListView(tableItemsDf)
    
    def _updateItemsListHeaderView(self, tableItemsDf):
        updatedHeader = self._createRow(tableItemsDf.columns)
        self.itemsViewLayout.replaceWidget(self._itemsListHeader, updatedHeader)
        self._itemsListHeader.deleteLater()
        self._itemsListHeader = updatedHeader
        # Another option to replace widget - will be left in case of problems with currebt solution
        # self.itemsViewLayout.removeWidget(self._itemsListHeader)
        # self._itemsListHeader.deleteLater()

        # self._itemsListHeader = self._createRow(tableItemsDf)
        # self.itemsViewLayout.insertWidget(len(self.itemsViewLayout) - 1, self._itemsListHeader)

    def _updateItemsListView(self, tableItemsDf):
        self.itemsList.clear()

        for index, dfRow in tableItemsDf.astype('str').iterrows():

            rowWidget = self._createRow(dfRow)

            item = QListWidgetItem()
            item.setSizeHint(rowWidget.sizeHint())  
            self.itemsList.addItem(item)
            self.itemsList.setItemWidget(item, rowWidget)

    def _createRow(self, dfRow):
        rowWidget = QWidget()
        rowWidget.setFixedWidth(400)
        rowLayout = QHBoxLayout()

        for cellValue in dfRow:
            cellLabel = QLabel(str(cellValue), rowWidget)
            cellLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

            rowLayout.addWidget(cellLabel)

        rowWidget.setLayout(rowLayout)
        
        return rowWidget
    
class ItemsFiltersView(QWidget):
    def __init__(self):
        super().__init__()

        self.filters = {}
        self._initView()

    def _initView(self):
        #Init layout wiith empty sublayout and button
        self.filtersViewLayout = QVBoxLayout()
        self.setLayout(self.filtersViewLayout)

        self.filtersLayout = QVBoxLayout()
        self.filterResultsButton = QPushButton("FILTRUJ")

        self.filtersViewLayout.addLayout(self.filtersLayout)
        self.filtersViewLayout.addWidget(self.filterResultsButton)

    def updateFiltersView(self, ItemsAttributes):
        #Clear Container of LineEdits and clear sublayout
        self.filtersLineEdits = {}

        while self.filtersLayout.count():
            item = self.filtersLayout.takeAt(0)
            if item is not None:
                while item.count():
                    subitem = item.takeAt(0)
                    widget = subitem.widget()
                    if widget is not None:
                        widget.setParent(None)
                self.filtersLayout.removeItem(item)
        #Refill sublayout with new layouts
        for attribute in ItemsAttributes:
            filterLayout = self._createFilter(attribute)
            self.filtersLayout.addLayout(filterLayout)
    
    def _createFilter(self, attribute):
        filterLayout = QHBoxLayout()

        filterLineEdits = {}

        limits = ['min', 'max']

        nameLabel = QLabel(attribute)
        nameLabel.setFixedWidth(50)
        filterLayout.addWidget(nameLabel)

        #Create LineEdits for every limit and set their input validation
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

            filterLayout.addLayout(limitLayout)
            filterLineEdits[limit] = limitLineEdit

        self.filtersLineEdits[attribute] = filterLineEdits
    
        return filterLayout

def main():
    dbApp = QApplication([])
    dbHandler = DatabaseHandler()
    
    window = Window()
    window.show()

    displayController = DBController(model=dbHandler, view=window)

    sys.exit(dbApp.exec())

if __name__ == "__main__":
    main()
