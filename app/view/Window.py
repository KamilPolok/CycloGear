from PyQt6.QtWidgets import (
    QComboBox,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from view.TableItemsView import TableItemsView
from view.ItemsFiltersView import ItemsFiltersView

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 500

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
