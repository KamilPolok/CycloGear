"""
    This file collects all functions that are common for each ITrackedTab class.
"""
from typing import Tuple

from PyQt6.QtWidgets import  QHBoxLayout, QLabel

from .Input import Input
from .Output import Output

from .ITrackedTab import ITrackedTab

def create_data_input_row(tab: ITrackedTab, attribute: str, description: str, symbol: str, decimal_precision: int=2) -> QHBoxLayout:
    """
    Create a row for data input with description, symbol, and input field.

    Args:
        tab (ITrackedTab): The tab where the row will be added.
        attribute (str): The attribute name corresponding to the data.
        description (str): The description of the attribute.
        symbol (str): The symbol representing the attribute.
    Returns:
        (QHBoxLayout): Layout containing the created widgets.
    """
    layout = QHBoxLayout()

    # Description label
    description_label = QLabel(description)
    description_label.setFixedWidth(150)
    description_label.setWordWrap(True)

    # Symbol label
    symbol_label = QLabel(f'{symbol} = ')
    symbol_label.setFixedWidth(50)

    # Input
    input = Input(tab)
    input.setDecimalPrecision(decimal_precision)
    input.setFixedWidth(80)
    if (value := tab.tab_data[attribute][0]) is not None:
        input.setText(str(value))

    # Units label
    units_label = QLabel(tab.tab_data[attribute][-1])
    units_label.setFixedWidth(50)

    # Assemble the layout
    layout.addWidget(description_label)
    layout.addWidget(symbol_label)
    layout.addWidget(input)
    layout.addWidget(units_label)

    # Save the line_edit for later reference
    tab.input_values[attribute] = input

    return layout

def create_data_display_row(tab: ITrackedTab, attribute: Tuple[int, str], data: list, symbol: str, description: str='', decimal_precision: int=2) -> QHBoxLayout:
    """
    Create a row for displaying data with description, symbol, and a read-only field.

    Args:
        tab (ITrackedTab): The tab where the row will be added.
        attribute (str): The attribute name corresponding to the data.
        data (list): The attribute data containing the value and unit.
        symbol (str): The symbol representing the attribute.
        description (str): The description of the attribute.
    Returns:
        (QHBoxLayout): Layout containing the created widgets.
    """
    layout = QHBoxLayout()

    # Description label
    description_label = QLabel(description)
    description_label.setFixedWidth(150)
    description_label.setWordWrap(True)

    # Symbol label
    symbol_label = QLabel(f'{symbol} = ')
    symbol_label.setFixedWidth(50)

    # Output
    output = Output(tab)
    output.setDecimalPrecision(decimal_precision)
    output.setFixedWidth(80)

    value = data[0]
    if value is not None:
        output.setValue(value)

    # Units label
    units_label = QLabel(data[-1])
    units_label.setFixedWidth(50)

    layout.addWidget(description_label)
    layout.addWidget(symbol_label)
    layout.addWidget(output)
    layout.addWidget(units_label)

    # Save the label for later reference
    tab.output_values[attribute] = output

    return layout
