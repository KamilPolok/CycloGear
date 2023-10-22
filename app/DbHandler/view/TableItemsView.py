from PyQt6.QtCore import Qt, pyqtSignal

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
class TableItemsView(QWidget):
    # Create a custom signal for passing the selected item attributes
    # It is needed for sending the selected item attributes outside the Window
    itemDataSignal = pyqtSignal(list)
    # Set Styles of the QTableWidget parts
    headerStyle = """
    QHeaderView::section {
        background-color: transparent;
        border: 0px;
        padding: 3px;
        margin: 0px;
    }
    QHeaderView::section:hover {
        background-color: transparent;
        border: 0px;
    }
    """
    selectedItemStyle = """
        QTableWidget::item:selected {
            background-color: lightgray;
            color: black;
        }
    """
    
    def __init__(self):
        super().__init__()

        self._initView()

    def _initView(self):
        # Set layout of TableItemsView
        self.itemsViewLayout = QVBoxLayout()
        self.itemsViewLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.itemsViewLayout)

        # Set sublayout of viewed table with items
        self.tablelayout = QHBoxLayout()
        self.itemsViewLayout.addLayout(self.tablelayout)

        # Set the viewed table
        self.itemsTable = QTableWidget()
        self.tablelayout.addWidget(self.itemsTable)

        self.itemsTable.setStyleSheet(self.headerStyle)

        ## Scrollbar settings
        self.itemsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.itemsTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        ## Headers settings
        self.itemsTable.horizontalHeader().setStyleSheet(self.selectedItemStyle)
        self.itemsTable.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

        self.itemsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.itemsTable.horizontalHeader().setHighlightSections(False)
        self.itemsTable.horizontalHeader().sectionPressed.disconnect()

        self.itemsTable.verticalHeader().hide()

        ## Cells settings
        self.itemsTable.setShowGrid(False)

        self.itemsTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.itemsTable.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.itemsTable.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.itemsTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def updateItemsView(self, tableItemsDf):
        # Prepare the items table based on parameters of the provided dataframe
        self.itemsTable.setRowCount(0)
        self.itemsTable.setColumnCount(len(tableItemsDf.columns))
        self.itemsTable.setHorizontalHeaderLabels(tableItemsDf.columns)
        # Fill in the itemsTable
        for rowIdx, rowData in tableItemsDf.astype('str').iterrows():
            self.itemsTable.insertRow(rowIdx)
            for col_idx, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                self.itemsTable.setItem(rowIdx, col_idx, item)
        # fit the geometry of the table to its contents
        self.setTableGeometry()
    
    def setTableGeometry(self):
        self.itemsTable.resizeColumnsToContents()
        # Set the width of the itemsTable
        tableWidth = sum([self.itemsTable.columnWidth(i) for i in range(self.itemsTable.columnCount())])
        tableWidth += 15    # Margin for srollbar width
        self.itemsTable.setFixedWidth(tableWidth)
        #TODO: find a better way to get the srollbar width
        # Set the maximum height of the itemsTable
        tableHeight = self.itemsTable.horizontalHeader().height()
        tableHeight += 2    # Margin for the summary height of cells frame
        tableHeight +=  self.itemsTable.rowCount() * self.itemsTable.rowHeight(0)
        
        self.itemsTable.setMaximumHeight(tableHeight)
    
    def emitItemDataSignal(self, item):
        # Get the selected item attributes
        itemData = [self.itemsTable.item(item.row(), col).text() for col in range(self.itemsTable.columnCount())]
        # Emit the custom signal
        self.itemDataSignal.emit(itemData)
