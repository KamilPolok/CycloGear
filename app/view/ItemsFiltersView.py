from PyQt6.QtCore import QRegularExpression

from PyQt6.QtGui import QRegularExpressionValidator

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class ItemsFiltersView(QWidget):
    def __init__(self):
        super().__init__()

        self.filters = {}
        self._initView()

    def _initView(self):
        #Init layout wiith empty sublayout and button
        self.filtersViewLayout = QVBoxLayout()
        self.setLayout(self.filtersViewLayout)

        self.filtersLayout = QVBoxLayout()
        self.filterResultsButton = QPushButton("FILTRUJ")

        self.filtersViewLayout.addLayout(self.filtersLayout)
        self.filtersViewLayout.addWidget(self.filterResultsButton)

    def updateFiltersView(self, ItemsAttributes):
        #Clear Container of LineEdits and clear sublayout
        self.filtersLineEdits = {}

        while self.filtersLayout.count():
            item = self.filtersLayout.takeAt(0)
            if item is not None:
                while item.count():
                    subitem = item.takeAt(0)
                    widget = subitem.widget()
                    if widget is not None:
                        widget.setParent(None)
                self.filtersLayout.removeItem(item)
        #Refill sublayout with new layouts
        for attribute in ItemsAttributes:
            filterLayout = self._createFilter(attribute)
            self.filtersLayout.addLayout(filterLayout)
    
    def _createFilter(self, attribute):
        filterLayout = QHBoxLayout()

        filterLineEdits = {}

        limits = ['min', 'max']

        nameLabel = QLabel(attribute)
        nameLabel.setFixedWidth(50)
        filterLayout.addWidget(nameLabel)

        #Create LineEdits for every limit and set their input validation
        for limit in limits:
            limitLayout = QHBoxLayout()
            limitLineEdit = QLineEdit()
            limitLineEdit.setFixedWidth(60)
            limitLineEdit.setMaxLength(8)
            reg_ex = QRegularExpression("[0-9]+\.?[0-9]+")
            input_validator = QRegularExpressionValidator(reg_ex, limitLineEdit)
            limitLineEdit.setValidator(input_validator)

            limitLabel = QLabel(limit)
            limitLabel.setFixedWidth(40)

            limitLayout.addWidget(limitLabel)
            limitLayout.addWidget(limitLineEdit)

            filterLayout.addLayout(limitLayout)
            filterLineEdits[limit] = limitLineEdit

        self.filtersLineEdits[attribute] = filterLineEdits
    
        return filterLayout
