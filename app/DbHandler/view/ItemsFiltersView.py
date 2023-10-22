from PyQt6.QtCore import Qt, QRegularExpression

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
        self.filtersViewLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.filtersViewLayout)

        self.filtersLayout = QVBoxLayout()
        self.filterResultsButton = QPushButton("FILTRUJ")

        self.filtersViewLayout.addLayout(self.filtersLayout)
        self.filtersViewLayout.addWidget(self.filterResultsButton)

    def updateFiltersView(self, ItemsAttributes):
        #Clear Container of LineEdits and remove Widgets from sublayout
        self.filtersLineEdits = {}
        for i in reversed(range(self.filtersLayout.count())): 
            self.filtersLayout.itemAt(i).widget().setParent(None)

        #Refill sublayout with new Widgets
        for attribute in ItemsAttributes:
            self._viewFilter(attribute)
            
    def _viewFilter(self, attribute):
        filterWidget = QWidget()

        filterLayout = QHBoxLayout()
        filterLayout.setContentsMargins(0, 0, 0, 0)
        filterWidget.setLayout(filterLayout)

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
            #Set input validation for LineEdit
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

        self.filtersLayout.addWidget(filterWidget)
