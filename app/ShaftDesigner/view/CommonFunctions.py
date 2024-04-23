import math

from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit


def create_data_input_row(symbol):
    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    # Symbol label
    symbol_label = QLabel(f'{symbol}')
    symbol_label.setFixedWidth(10)
    font = QFont()
    font.setBold(True)
    font.setItalic(True)
    symbol_label.setFont(font)

    # Line edit for input
    line_edit = QLineEdit()
    line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
    line_edit.setFixedWidth(100)
    line_edit.setText('')
    
    # Input validation
    regex = QRegularExpression(r'^[0-9]\d{0,3}(\.\d{1,2})?$')
    line_edit.setValidator(QRegularExpressionValidator(regex, line_edit))

    # Units label
    units_label = QLabel('mm')
    units_label.setFixedWidth(25)

    # Assemble the layout
    layout.addWidget(symbol_label)
    layout.addWidget(line_edit)
    layout.addWidget(units_label)

    return (layout, line_edit)

def is_number(variable):
    try:
        float(variable)
        return True
    except ValueError:
        return False

# Format a number to float with 2 decimal digits
def format_input(variable):
    if is_number(variable):
        return '{:.2f}'.format(float(variable))
    else:
        return None  # Or return None
