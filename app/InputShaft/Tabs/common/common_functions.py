"""
    This file collects all functions that are common for each ITrackedTab class.
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QFrame, QSizePolicy, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from .Input import Input
from .Output import Output

def _create_entrypoint_row(entrypoint: QLineEdit, data: list, symbol: str, description: str, decimal_precision: int) -> QFrame:
    """
    Create a row for data entrypoint with description, symbol, and input field.

    Args:
        entrypoint (QLineEdit): Input or Output
        data (list): List holding the attribute value and unit.
        description (str): The description of the attribute.
        symbol (str): The symbol representing the attribute.
    Returns:
        row (QFrame): row containing the created widgets.
    """
    row = QFrame()
    row.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    layout = QHBoxLayout()
    layout.setContentsMargins(5, 5, 5, 5)

    layout.setSpacing(5)
    row.setLayout(layout)

    # Description label
    description_label = QLabel(description)
    description_label.setMinimumWidth(100)
    description_label.setWordWrap(True)

    # Symbol label
    symbol_label = QLabel(symbol)
    symbol_label.setFixedWidth(30)
    symbol_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    symbol_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

    # Equals sign
    equals_sign = QLabel('=')
    equals_sign.setFixedWidth(20)
    equals_sign.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Entrypoint
    entrypoint.setParent(row)
    entrypoint.setDecimalPrecision(decimal_precision)
    entrypoint.setFixedWidth(100)

    value = data[0]
    if value is not None:
        entrypoint.setValue(value)

    # Units label
    units_label = QLabel(data[-1])
    units_label.setFixedWidth(50)

    # Assemble the layout
    layout.addWidget(description_label)
    layout.addWidget(symbol_label)
    layout.addWidget(equals_sign)
    layout.addWidget(entrypoint)
    layout.addWidget(units_label)

    # Save the label for later reference
    data[0] = entrypoint

    return row

def create_data_input_row(data: list, symbol: str, description: str, decimal_precision: int=2) -> QFrame:
    input = Input()
    return _create_entrypoint_row(input, data, symbol, description, decimal_precision)

def create_data_display_row(data: list, symbol: str, description: str='', decimal_precision: int=2) -> QFrame:
    output = Output()
    return _create_entrypoint_row(output, data, symbol, description, decimal_precision)

def create_header(text, size=10, font='Arial', bold=False):
    header = QLabel(text)
    font = QFont(font, size)
    font.setBold(bold)
    header.setFont(font)

    return header
