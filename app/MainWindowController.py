from DbHandler.controller.DBController import ViewSelectItemController, ViewDbTablesController
from DbHandler.model.DatabaseHandler import DatabaseHandler
from DbHandler.view.Window import Window

class MainWindowController:
    def __init__(self, view):
        self._mainWindow = view

        self._connectSignalsAndSlots()

    def _connectSignalsAndSlots(self):
        self._mainWindow.selectItemBtn.clicked.connect(self._openViewSelectItemsWindow)
        self._mainWindow.openItemsCatalogBtn.clicked.connect(self._openViewDbTablesWindow)

    def _openViewSelectItemsWindow(self):
        # # Get acces to the database
        dbHandler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subWindow = Window()
        subWindow.setWindowTitle("Łożyska osadzone na tarczy")
        # Specify the group name of the tables you want to take for consideration
        tablesGroupName = 'łożyska-tarcza'
        availableTables = dbHandler.getAvailableTables(tablesGroupName)
        # Specify the limits for the group of tables
        limits = dbHandler.getTableItemsFilters(tablesGroupName)
        # Set some dummy limits - in the reality those values will be calculated
        limits["Dz"]["min"] = 25
        limits["Dz"]["max"] = 48
        # Setup the controller for the subwindow
        viewSelectItemsCtrl = ViewSelectItemController(dbHandler, subWindow, availableTables, limits)
        subWindow.itemDataSignal.connect(self._printItemData)
        subWindow.exec()
    
    def _openViewDbTablesWindow(self):
       # Get acces to the database
        dbHandler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subWindow = Window()
        subWindow.setWindowTitle("Katalog gotowych elementów")
        # Setup the controller for the subwindow
        viewDbTablesCtrl = ViewDbTablesController(dbHandler, subWindow)
        subWindow.exec()

    def _printItemData(self, itemData):
        print(itemData)