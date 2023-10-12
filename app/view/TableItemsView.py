from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

class TableItemsView(QWidget):
    def __init__(self):
        super().__init__()

        self._initView()

    def _initView(self):
        #Init layout with dummy widget and empty list widget
        self.itemsViewLayout = QVBoxLayout()
        self.setLayout(self.itemsViewLayout)

        self._itemsListHeader = QWidget()
        self.itemsList = QListWidget()
        
        self.itemsViewLayout.addWidget(self._itemsListHeader)
        self.itemsViewLayout.addWidget(self.itemsList)

    def updateItemsView(self, tableItemsDf):
        self._updateItemsListHeaderView(tableItemsDf)
        self._updateItemsListView(tableItemsDf)
    
    def _updateItemsListHeaderView(self, tableItemsDf):
        updatedHeader = self._createRow(tableItemsDf.columns)
        self.itemsViewLayout.replaceWidget(self._itemsListHeader, updatedHeader)
        self._itemsListHeader.deleteLater()
        self._itemsListHeader = updatedHeader
        # Another option to replace widget - will be left in case of problems with currebt solution
        # self.itemsViewLayout.removeWidget(self._itemsListHeader)
        # self._itemsListHeader.deleteLater()

        # self._itemsListHeader = self._createRow(tableItemsDf)
        # self.itemsViewLayout.insertWidget(len(self.itemsViewLayout) - 1, self._itemsListHeader)

    def _updateItemsListView(self, tableItemsDf):
        self.itemsList.clear()

        for index, dfRow in tableItemsDf.astype('str').iterrows():

            rowWidget = self._createRow(dfRow)

            item = QListWidgetItem()
            item.setSizeHint(rowWidget.sizeHint())  
            self.itemsList.addItem(item)
            self.itemsList.setItemWidget(item, rowWidget)

    def _createRow(self, dfRow):
        rowWidget = QWidget()
        rowWidget.setFixedWidth(400)
        rowLayout = QHBoxLayout()

        for cellValue in dfRow:
            cellLabel = QLabel(str(cellValue), rowWidget)
            cellLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

            rowLayout.addWidget(cellLabel)

        rowWidget.setLayout(rowLayout)
        
        return rowWidget
