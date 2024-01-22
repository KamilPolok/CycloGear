from ast import literal_eval

from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit


def create_data_input_row(attribute, symbol):
    layout = QHBoxLayout()
    
    # Symbol label
    symbol_label = QLabel(f'{symbol}')
    symbol_label.setFixedWidth(10)

    equals_sign = QLabel('=')
    equals_sign.setFixedWidth(10)

    # Line edit for input
    line_edit = QLineEdit()
    line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
    line_edit.setFixedWidth(50)
    line_edit.setText('')
    
    # Input validation
    regex = QRegularExpression(r'^[0-9]\d{0,3}(\.\d{1,2})?$')
    line_edit.setValidator(QRegularExpressionValidator(regex, line_edit))

    # Units label
    units_label = QLabel('mm')
    units_label.setFixedWidth(25)

    # Assemble the layout
    layout.addWidget(symbol_label)
    layout.addWidget(equals_sign)
    layout.addWidget(line_edit)
    layout.addWidget(units_label)

    return (layout, line_edit)
