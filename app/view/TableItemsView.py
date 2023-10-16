from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
class TableItemsView(QWidget):
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
       
        #Set layout of TableItemsView
        self.itemsViewLayout = QVBoxLayout()
        self.itemsViewLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.itemsViewLayout)

        #Set sublayout of viewed table with items
        self.tablelayout = QHBoxLayout()
        self.itemsViewLayout.addLayout(self.tablelayout)

        #Set the viewed table
        self.itemsTable = QTableWidget()
        self.tablelayout.addWidget(self.itemsTable)

        self.itemsTable.setStyleSheet(self.headerStyle)

        ##Scrollbar settings
        self.itemsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.itemsTable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        ##Headers settings
        self.itemsTable.horizontalHeader().setStyleSheet(self.selectedItemStyle)
        self.itemsTable.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

        self.itemsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.itemsTable.horizontalHeader().setHighlightSections(False)
        self.itemsTable.horizontalHeader().sectionPressed.disconnect()

        self.itemsTable.verticalHeader().hide()

        ##Cells settings
        self.itemsTable.setShowGrid(False)

        self.itemsTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.itemsTable.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.itemsTable.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.itemsTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def updateItemsView(self, tableItemsDf):
        self.itemsTable.setRowCount(0)
        self.itemsTable.setColumnCount(len(tableItemsDf.columns))
        self.itemsTable.setHorizontalHeaderLabels(tableItemsDf.columns)

        for rowIdx, rowData in tableItemsDf.astype('str').iterrows():
            self.itemsTable.insertRow(rowIdx)
            for col_idx, value in enumerate(rowData):
                item = QTableWidgetItem(str(value))
                self.itemsTable.setItem(rowIdx, col_idx, item)

        self.setTableGeometry()
    
    def setTableGeometry(self):
        self.itemsTable.resizeColumnsToContents()

        tableWidth = sum([self.itemsTable.columnWidth(i) for i in range(self.itemsTable.columnCount())])
        tableWidth += 15    #margin for srollbar width
        self.itemsTable.setFixedWidth(tableWidth)

        tableHeight = self.itemsTable.horizontalHeader().height() + 2
        tableHeight +=  self.itemsTable.rowCount() * self.itemsTable.rowHeight(0)
        
        self.itemsTable.setMaximumHeight(tableHeight)
