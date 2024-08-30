from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QPalette

from PyQt6.QtWidgets import (
    QMenu,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

class TablesTreeView(QWidget):
    # Create a custom signal for passing the selected table name
    tableSelectedSignal = pyqtSignal(str) 

    def __init__(self, availableTables):
        super().__init__()
        self._availableTables = availableTables
        # Set active table
        self.activeTable = availableTables[0]
        # Parse and structure the table names
        self._organizeTables(availableTables)
        # Init view
        self._initView()
    
    def _emitSelectedTable(self, item, column):
        activeTable = item.data(0, Qt.ItemDataRole.UserRole)  # Get the data from column 0
        self.tableSelectedSignal.emit(activeTable)  # Emit the custom signal with table name
    
    def _findItemByData(self, tree, value):
        model = tree.model()
        matches = model.match(model.index(0, 0), Qt.ItemDataRole.UserRole, value, 1, Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive)
        if matches:
            return tree.itemFromIndex(matches[0])
        return None

    def _resetTablesTree(self):
        def clearItemHighlightAndCollapse(item):
            for i in range(item.columnCount()):
                item.setBackground(i, QBrush())
            for j in range(item.childCount()):
                child = item.child(j)
                clearItemHighlightAndCollapse(child)
                child.setExpanded(False)

        # Go through every toplevel branch            
        for i in range(self.tablesTree.topLevelItemCount()):
            topLevelItem = self.tablesTree.topLevelItem(i)
            # Recursively collapse an clear highlight for every branch in the toplevel branch
            clearItemHighlightAndCollapse(topLevelItem)
            # Colapse toplevel branch
            topLevelItem.setExpanded(False)

    def _organizeTables(self, tables):
        # Parse and organize the tables in form of a dictionary tree
        self.organizedTables = {}
        # Create a dictionary of table categories for every table
        self.tableCategories = {}

        for table in tables:
            categories = table.split('-')
            d = self.organizedTables
            for category in categories[:-1]:
                d = d.setdefault(category, {})
            d[categories[-1]] = table
        
            self.tableCategories[table] = categories
    
    def _openOnActiveTable(self):
        # Reset the view of table tree to default
        self._resetTablesTree()
        
        # get QTreeWidgetItem for the active table from the tree
        item = self._findItemByData(self.tablesTree, self.activeTable)
        if item:
            # Highlight the current active table
            highlightColor = self.palette().color(QPalette.ColorRole.Mid)
            for i in range(item.columnCount()):
                item.setBackground(i, highlightColor)
            # Expand the tree branches to the active table
            while item:
                item.setExpanded(True)
                item = item.parent()
    
    def _fillTablesTree(self, parent, value):
        # fill the the table tree with tables from dictionary
        if isinstance(value, dict):
            for key, val in value.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, key)
                self._fillTablesTree(item, val)
        else:
            # If get to the leaf set its data to the table name
            parent.setData(0, Qt.ItemDataRole.UserRole, value)

    def _setActiveTableBtnText(self):
        # Set the names for every column in the tree
        index_to_name = {
            0: "elementy",
            1: "miejsce",
            2: "rodzaj"
        }
        # Set text for the button accoridng to the active table
        categories = self.tableCategories[self.activeTable]
        label_text = "".join([f"{index_to_name.get(idx)}:\t{part}\n" for idx, part in enumerate(categories)])
        label_text = label_text.rstrip()
        self.activeTableBtn.setText(label_text)
    
    def _initView(self):
        # Set layout
        self.tableTreeViewLayout = QVBoxLayout()
        self.setLayout(self.tableTreeViewLayout)
        # Set a tree view of available tables
        self.tablesTree = QTreeWidget(self)
        self.tablesTree.setHeaderHidden(True)
        self._fillTablesTree(self.tablesTree, self.organizedTables)
        # Set dropdown menu and add the tree to it
        self.menu = QMenu(self)
        treeWidgetAction = QWidgetAction(self.menu)
        treeWidgetAction.setDefaultWidget(self.tablesTree)
        self.menu.addAction(treeWidgetAction) 
        # Set a button displaying the active table and opening the dropdown menu
        self.activeTableBtn = QPushButton()
        self.activeTableBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.activeTableBtn.setStyleSheet("text-align: left;")
        self._setActiveTableBtnText()
        self.activeTableBtn.setMenu(self.menu)
        self.tableTreeViewLayout.addWidget(self.activeTableBtn)
        # Connect the signals
        self.tablesTree.itemClicked.connect(self._emitSelectedTable)
        self.menu.aboutToShow.connect(self._openOnActiveTable)
    
    def updateActiveTable(self, activeTable):
        self.activeTable = activeTable
        self._setActiveTableBtnText()
        self.menu.hide()
