import sys

from PyQt6.QtWidgets import(
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
)

from controller.DBController import ViewSelectItemController, ViewDbTablesController
from model.DatabaseHandler import DatabaseHandler
from view.Window import Window

MAIN_WINDOW_W = 300
MAIN_WINDOW_H = 100

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
        # Connect a method that will use the data passed by signal from the subwindow
        viewSelectItemsCtrl._window.TableItemsView.itemDataSignal.connect(self._printItemData)
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mechkonstruktor 2.0")
        self.setFixedSize(MAIN_WINDOW_W, MAIN_WINDOW_H)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        self._initView()

    def _initView(self):
        self.selectItemBtn = QPushButton("Wybierz łożysko")
        self.openItemsCatalogBtn = QPushButton("Otwórz katalog znormalizowanych elementów")

        self.generalLayout.addWidget(self.selectItemBtn)
        self.generalLayout.addWidget(self.openItemsCatalogBtn)

def main():
    dbApp = QApplication([])

    mainWindow = MainWindow()
    mainWindowCtrl = MainWindowController(mainWindow)
    mainWindow.show()

    sys.exit(dbApp.exec())

if __name__ == "__main__":
    main()
