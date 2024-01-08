from ast import literal_eval

from PyQt6.QtCore import Qt, QRegularExpression, pyqtSignal
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget

class ShaftSubsection(QWidget):
    subsection_data_signal = pyqtSignal(dict)
    remove_subsection_signal = pyqtSignal(int)

    def __init__(self, section_name, subsection_number, parent=None):
        super().__init__(parent)
        self.section_name = section_name
        self.subsection_number = subsection_number
        self.expanded = False
        self.input_values = {}
        self.limits = {}

        self._init_ui()

    def _init_ui(self):
        # Set layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Set header
        self.header = QLabel()
        self._set_header()
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setFixedHeight(30)
        self.header.mousePressEvent = self.toggle
        self.main_layout.addWidget(self.header)

        # Set content widget and layout
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Set data entries
        diameter = self._create_data_input_row('d', 'Ø')
        length = self._create_data_input_row('l', 'L')

        # Set OK button
        self.confirm_button = QPushButton("OK", self)
        self.confirm_button.clicked.connect(self.emit_data_signal)
        self.confirm_button.setEnabled(False)

        # Set removal button
        self.remove_button = QPushButton("Usuń", self)
        self.remove_button.clicked.connect(self.emit_remove_signal)

        self.content_layout.addLayout(diameter)
        self.content_layout.addLayout(length)
        self.content_layout.addWidget(self.confirm_button)
        self.content_layout.addWidget(self.remove_button)
        self.content_widget.setVisible(False)

        self.main_layout.addWidget(self.content_widget)

        # Initially collapse ShaftSubsection widget
        self.expanded = True
        self.toggle(None)
    
    def _set_header(self):
        self.header.setText(f'{self.subsection_number + 1}.')
          
    def _create_data_input_row(self, attribute, symbol):
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

        # Save the line_edit for later reference
        self.input_values[attribute] = line_edit
        self.limits[attribute] = {'min': None, 'max': None}

        # Connect signals and slots
        self.input_values[attribute].textChanged.connect(self.check_if_all_inputs_provided)
        self.input_values[attribute].editingFinished.connect(self._check_boundaries)

        return layout

    def format_input(self, number):
        # Check if the text is a valid number and set its format
        if number is None:
            formatted_text = ""
        else:
            formatted_text = "{:.2f}".format(number)
        
        return formatted_text

    def _check_boundaries(self, line_edit=None):
        # Check if the input value is within bounadaries
        if line_edit is None:
            line_edit = self.sender()
        line_edit_key = next((key for key, value in self.input_values.items() if value == line_edit), None)
       
        min_value = self.limits[line_edit_key]['min']
        max_value = self.limits[line_edit_key]['max']
        value = float(line_edit.text()) if line_edit.text() else None

        if line_edit_key == 'd':
            if min_value is not None and (value is None or value < min_value):
                line_edit.setText(self.format_input(min_value))
            elif max_value is not None and value is not None and value > max_value:
                line_edit.setText(self.format_input(max_value))
            else:
                line_edit.setText(self.format_input(value))
            line_edit.setPlaceholderText(self.format_input(min_value))
        elif line_edit_key == 'l':
            if min_value is not None and value is not None and value < min_value:
                line_edit.setText(self.format_input(min_value))
            elif max_value is not None and (value is None or value > max_value):
                line_edit.setText(self.format_input(max_value))
            else:
                line_edit.setText(self.format_input(value))

    def set_attributes(self, attributes):
        for attribute, value in attributes.items():
            if value is not None:
                self.input_values[attribute].setText(self.format_input(value))
    
    def set_limits(self, attribute, limits):
        self.limits[attribute]['min'] = limits['min']
        self.limits[attribute]['max'] =  limits['max']
        self._check_boundaries(self.input_values[attribute])

    def get_attributes(self):
        return {self.section_name: {self.subsection_number: {key: literal_eval(input.text()) for key, input in self.input_values.items()}}}

    def set_read_only(self, attribute):
        self.input_values[attribute].setReadOnly(True)
    
    def update_subsection_name(self, new_number):
        self.subsection_number = new_number
        self._set_header()
    
    def toggle(self, event):
        # Collapse or expand contents of section
        self.expanded = not self.expanded
        self.content_widget.setVisible(self.expanded)

        self.adjustSize()
        self.updateGeometry()

    def check_if_all_inputs_provided(self):
        self.confirm_button.setEnabled(all(input.text() != '' for input in self.input_values.values()) and all(literal_eval(input.text()) != 0 for input in self.input_values.values()))

    def emit_data_signal(self):
        self.subsection_data_signal.emit(self.get_attributes())
    
    def emit_remove_signal(self):
        self.remove_subsection_signal.emit(self.subsection_number)
