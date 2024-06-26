from ast import literal_eval
from functools import partial

class ViewSelectItemController:
    def __init__(self, model, view, availableTables, limits):
        self._dbHandler = model
        self._window = view
        self._availableTables = availableTables
        self._limits = limits

        self.selectedItemAttributes = None
        self._initUI()
        self._connectSignalsAndSlots()

    def _initUI(self):
        # Set active table
        self._activeTable = self._availableTables[0]
        # Init view
        self._window.viewActiveTableSelector(self._availableTables)
        self._window.viewTableItems(self._dbHandler.getFilteredResults(self._activeTable, self._limits))
        self._window.viewFunctionButtons()

    def _connectSignalsAndSlots(self):
        self._window.TableItemsView.itemsTable.itemClicked.connect(self._selectItemEvent)
        self._window.activeTableSelector.currentIndexChanged.connect(self._switchActiveTableEvent)
        self._window.okBtn.clicked.connect(partial(self._closeWindowEvent, True))
        self._window.cancelBtn.clicked.connect(partial(self._closeWindowEvent, False))

    def _switchActiveTableEvent(self, selectedTableIndex):
        # Check if selected table is not active table
        selectedTable = self._availableTables[selectedTableIndex]
        if self._activeTable is not selectedTable:
            # Set new active table
            self._activeTable = selectedTable
            # Update view
            updatedResults = self._dbHandler.getFilteredResults(self._activeTable, self._limits)
            self._window.TableItemsView.updateItemsView(updatedResults)

    def _selectItemEvent(self, item):
        # Get the selected item attributes
        itemCode = self._window.TableItemsView.getItemCode(item)
        itemData = self._dbHandler.getSingleItem(self._activeTable, itemCode)
        self.selectedItemAttributes = itemData
        # Enable the OK button
        self._window.okBtn.setEnabled(True)
    
    def _closeWindowEvent(self, itemSelected):
        if itemSelected:
            self._window.accept()
        else:
            self._window.reject()
    
    def startup(self):
        result = self._window.exec()
        return result == self._window.DialogCode.Accepted

class ViewDbTablesController:
    def __init__(self, model, view):
        self._dbHandler = model
        self._window = view
        
        self._startup()
        self._connectSignalsAndSlots()
    
    def _startup(self):
        # Set active table
        self._availableTables = self._dbHandler.getAvailableTables()
        self._activeTable = self._availableTables[0]
        # Get limits
        self._limits = self._dbHandler.getTableItemsFilters(self._activeTable)
        # Init view
        self._window.viewTablesTree(self._availableTables)
        self._window.viewFilters(self._dbHandler.getTableItemsAttributes(self._activeTable))
        self._window.viewTableItems(self._dbHandler.getFilteredResults(self._activeTable, self._limits))
    
    def _connectSignalsAndSlots(self):
        self._window.tablesTreeView.tableSelectedSignal.connect(self._switchActiveTableEvent)
        self._window.ItemsFiltersView.filterResultsButton.clicked.connect(self._updateResultsEvent)
    
    def _switchActiveTableEvent(self, selectedTable):
        # Check if selected table is not active table
        if selectedTable and self._activeTable is not selectedTable:
            # Set new active table
            self._activeTable = selectedTable
            # Update limits - get them from new active table
            self._limits = self._dbHandler.getTableItemsFilters(self._activeTable)
            # Update view
            updatedResults = self._dbHandler.getFilteredResults(self._activeTable, self._limits)
            updatedAttributes = self._dbHandler.getTableItemsAttributes(self._activeTable)
            self._window.TableItemsView.updateItemsView(updatedResults)
            self._window.ItemsFiltersView.updateFiltersView(updatedAttributes)
            self._window.tablesTreeView.updateActiveTable(self._activeTable)

    def _updateResultsEvent(self):
        # Update limits - get them from user inputs
        for attribute, attributeLimits in self._limits.items():
            for limit in attributeLimits:
                text = self._window.ItemsFiltersView.filtersLineEdits[attribute][limit].text()
                number = literal_eval(text) if text else 0
                attributeLimits[limit] = number
        # Update items view
        updatedResults = self._dbHandler.getFilteredResults(self._activeTable, self._limits)
        self._window.TableItemsView.updateItemsView(updatedResults)
