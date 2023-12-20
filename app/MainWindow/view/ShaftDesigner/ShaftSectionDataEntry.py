from ast import literal_eval

from PyQt6.QtCore import QRegularExpression, pyqtSignal
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget

class ShaftSectionDataEntry(QWidget):
    attributes_signal = pyqtSignal(dict)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.expanded = False
        self.input_values = {}

        self._init_ui()

    def _init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Set header
        self.header = QLabel(self.name)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setFixedHeight(30)
        self.header.mousePressEvent = self.toggle
        self.main_layout.addWidget(self.header)

        # Set content widget and layout
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        diameter = self._create_data_input_row('d', 'Ø')
        length = self._create_data_input_row('l', 'L')

        self.confirm_button = QPushButton("OK", self)
        self.confirm_button.clicked.connect(self.emit_attributes)
        self.confirm_button.setEnabled(False)

        self.content_layout.addLayout(diameter)
        self.content_layout.addLayout(length)
        self.content_layout.addWidget(self.confirm_button)
        self.content_widget.setVisible(False)

        self.main_layout.addWidget(self.content_widget)
    
    def _create_data_input_row(self, attribute, symbol):
        layout = QHBoxLayout()
        
        # Symbol label
        symbol_label = QLabel(f'{symbol}')
        symbol_label.setFixedWidth(10)

        equals_sign = QLabel('=')
        equals_sign.setFixedWidth(10)

        # Line edit for input
        line_edit = QLineEdit()
        line_edit.setFixedWidth(50)
        line_edit.setText('')
        
        # Input validation
        regex = QRegularExpression(r'^[1-9]\d{0,3}(\.\d{1,2})?$')
        line_edit.setValidator(QRegularExpressionValidator(regex, line_edit))

        # Units label
        units_label = QLabel('mm')
        units_label.setFixedWidth(25)

        # Assemble the layout
        layout.addWidget(symbol_label)
        layout.addWidget(equals_sign)
        layout.addWidget(line_edit)
        layout.addWidget(units_label)

        # Save the line_edit for later reference
        self.input_values[attribute] = line_edit

        # Connect textChanged signal
        self.input_values[attribute].textChanged.connect(self.check_line_edits)

        return layout
    
    def set_attributes(self, attributes, readonly = []):
        for attribute, value in attributes.items():
            if value is not None:
                self.input_values[attribute].setText(str(value))

    def set_read_only(self, attribute):
        self.input_values[attribute].setReadOnly(True)

    def toggle(self, event):
        # Collapse or expand contents of section
        self.expanded = not self.expanded
        self.content_widget.setVisible(self.expanded)

        self.adjustSize()
        self.updateGeometry()

    def check_line_edits(self):
        self.confirm_button.setEnabled(all(input.text() != '' for input in self.input_values.values()))

    def emit_attributes(self):
        self.attributes_signal.emit({self.name: {key: literal_eval(input.text()) for key, input in self.input_values.items()}})
