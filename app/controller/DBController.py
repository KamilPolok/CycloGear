from ast import literal_eval

from PyQt6.QtWidgets import QLabel

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
        itemData = [self._window.TableItemsView.itemsTable.item(item.row(), col).text() for col in range(self._window.TableItemsView.itemsTable.columnCount())]
        print(itemData)

    def _connectSignalsAndSlots(self):
        self._window.activeTableSelector.activated.connect(self._switchActiveTableEvent)
        self._window.ItemsFiltersView.filterResultsButton.clicked.connect(self._updateResultsEvent)
        self._window.TableItemsView.itemsTable.itemClicked.connect(self._selectItemEvent)
