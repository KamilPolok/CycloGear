from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

from .TableItemsView import TableItemsView
from .ItemsFiltersView import ItemsFiltersView
from .TablesTreeView import TablesTreeView

class Window(QDialog):
    # Create a custom signal for passing the selected item attributes
    # It is needed for sending the selected item attributes outside the Window
    def __init__(self, parent):
        super().__init__(parent)
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

    def viewActiveTableSelector(self, availableTables):
        # Create a collapsable list for choosing active table
        self.activeTableSelector = QComboBox()
        # Get the items type from tables names (tables are of the same group) 
        organizedTables = {item.split('-')[-1]: item for item in availableTables}

        for key, table in organizedTables.items():
             self.activeTableSelector.addItem(key)

        self.generalLayout.addWidget(self.activeTableSelector)

    def viewTablesTree(self, availableTables):
        self.tablesTreeView = TablesTreeView(availableTables)

        self.generalLayout.addWidget(self.tablesTreeView)

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
