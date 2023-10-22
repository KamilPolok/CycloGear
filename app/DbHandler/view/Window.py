from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
)

from .TableItemsView import TableItemsView
from .ItemsFiltersView import ItemsFiltersView

class Window(QDialog):
    # Create a custom signal for passing the selected item attributes
    # It is needed for sending the selected item attributes outside the Window
    itemDataSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

    def _organizeTables(self, tables):
        # Parse and organize the tables in form of a dictionary tree
        organizedTables = {}

        for table in tables:
            parts = table.split('-')
            d = organizedTables
            for part in parts[:-1]:
                d = d.setdefault(part, {})
            d[parts[-1]] = table

        return organizedTables

    def _fillTabLeTree(self, parent, value):
        if isinstance(value, dict):
            for key, val in value.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, key)
                self._fillTabLeTree(item, val)
        else:
            parent.setData(0, 1, value)
    
    def viewActiveTableSelector(self, availableTables):
        # Create a collapsable list for choosing active table
        self.activeTableSelector = QComboBox()
        # Get the items type from tables names (tables are of the same group) 
        organizedTables = {item.split('-')[-1]: item for item in availableTables}

        for key, table in organizedTables.items():
             self.activeTableSelector.addItem(key)

        self.generalLayout.addWidget(self.activeTableSelector)

    def viewTableTree(self, availableTables):
        # Parse and structure the table names
        organizedTables = self._organizeTables(availableTables)
        # Create a tree view of available tables divided by groups    
        self.tableTree = QTreeWidget(self)
        self.tableTree.setHeaderHidden(True)
        self._fillTabLeTree(self.tableTree, organizedTables)

        self.generalLayout.addWidget(self.tableTree)

    def viewFilters(self, tableAttributes):
        # View filters for given table
        self.ItemsFiltersView = ItemsFiltersView()
        self.ItemsFiltersView.updateFiltersView(tableAttributes)

        self.generalLayout.addWidget(self.ItemsFiltersView)

    def viewTableItems(self, tableItemsDf):
        # View items from given table
        self.TableItemsView = TableItemsView()
        self.TableItemsView.updateItemsView(tableItemsDf)

        self.generalLayout.addWidget(self.TableItemsView)

    def viewFunctionButtons(self):
        # View OK and Cancel buttons
        FunctionBtnsLayout = QHBoxLayout()
    
        self.okBtn = QPushButton("OK", self)
        self.okBtn.setEnabled(False)
        
        self.cancelBtn = QPushButton("Anuluj", self)

        FunctionBtnsLayout.addWidget(self.okBtn)
        FunctionBtnsLayout.addWidget(self.cancelBtn)

        self.generalLayout.addLayout(FunctionBtnsLayout)

    def emitItemDataSignal(self, itemData):
        # Emit signal with data from selected item
        self.itemDataSignal.emit(itemData)
