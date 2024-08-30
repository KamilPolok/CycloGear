from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QFont
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit

def createDataInputRow(symbol):
    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    # Symbol label
    symbolLabel = QLabel(f'{symbol}')
    symbolLabel.setFixedWidth(10)
    font = QFont()
    font.setBold(True)
    font.setItalic(True)
    symbolLabel.setFont(font)

    # Line edit for input
    lineEdit = QLineEdit()
    lineEdit.setAlignment(Qt.AlignmentFlag.AlignRight)
    lineEdit.setFixedWidth(100)
    lineEdit.setText('')
    
    # Input validation
    regex = QRegularExpression(r'^[0-9]\d{0,3}(\.\d{1,2})?$')
    lineEdit.setValidator(QRegularExpressionValidator(regex, lineEdit))

    # Units label
    unitsLabel = QLabel('mm')
    unitsLabel.setFixedWidth(25)

    # Assemble the layout
    layout.addWidget(symbolLabel)
    layout.addWidget(lineEdit)
    layout.addWidget(unitsLabel)

    return (layout, lineEdit)

def isNumber(variable):
    try:
        float(variable)
        return True
    except ValueError:
        return False

# Format a number to float with 2 decimal digits
def formatInput(variable):
    if isNumber(variable):
        return '{:.2f}'.format(float(variable))
    else:
        return None  # Or return None
