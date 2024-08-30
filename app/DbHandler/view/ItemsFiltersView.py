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
        # Init layout wiith empty sublayout and button
        filtersViewLayout = QVBoxLayout()
        filtersViewLayout.setContentsMargins(0,0,0,0)
        self.setLayout(filtersViewLayout)

        self.filtersLayout = QVBoxLayout()
        self.filterResultsButton = QPushButton("FILTRUJ")

        filtersViewLayout.addLayout(self.filtersLayout)
        filtersViewLayout.addWidget(self.filterResultsButton)

    def _viewFilter(self, attribute):
        filterWidget = QWidget()

        filterLayout = QHBoxLayout()
        filterLayout.setContentsMargins(0, 0, 0, 0)
        filterWidget.setLayout(filterLayout)

        filterLineEdits = {}

        limits = ['min', 'max']

        nameLabel = QLabel(attribute[0])
        nameLabel.setFixedWidth(35)
        filterLayout.addWidget(nameLabel)

        # Create LineEdits for every limit and set their input validation
        for limit in limits:
            limitLayout = QHBoxLayout()

            limitLineEdit = QLineEdit()
            limitLineEdit.setFixedWidth(60)
            limitLineEdit.setMaxLength(8)
            # Set input validation for LineEdit
            regex = QRegularExpression("[0-9]+\.?[0-9]+")
            inputValidator = QRegularExpressionValidator(regex, limitLineEdit)
            limitLineEdit.setValidator(inputValidator)

            limitLabel = QLabel(limit)
            limitLabel.setFixedWidth(30)

            limitLayout.addWidget(limitLabel)
            limitLayout.addWidget(limitLineEdit)

            filterLayout.addLayout(limitLayout)
            filterLineEdits[limit] = limitLineEdit
        
        unitLabel = QLabel(attribute[1])
        unitLabel.setFixedWidth(50)
        filterLayout.addWidget(unitLabel)

        self.filtersLineEdits[attribute[0]] = filterLineEdits

        self.filtersLayout.addWidget(filterWidget)

    def updateFiltersView(self, itemsAttributes):
        # Clear Container of LineEdits and remove Widgets from sublayout
        self.filtersLineEdits = {}
        for i in reversed(range(self.filtersLayout.count())): 
            self.filtersLayout.itemAt(i).widget().setParent(None)

        # Refill sublayout with new Widgets
        for attribute in itemsAttributes:
            self._viewFilter(attribute)
