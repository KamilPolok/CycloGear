from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from .CommonFunctions import create_data_input_row, format_input

class ShaftSubsection(QWidget):
    subsection_data_signal = pyqtSignal(dict)
    remove_subsection_signal = pyqtSignal(int)

    def __init__(self, section_name, subsection_number, parent=None):
        super().__init__(parent)
        self.section_name = section_name
        self.subsection_number = subsection_number
        self.expanded = False
        self.inputs = {}
        self.limits = {}

        self._init_ui()

    def _init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self._init_header()
        self._init_content()

    def _init_header(self):
        # Header layout
        self.header_layout = QHBoxLayout()
        self.main_layout.addLayout(self.header_layout)

        # Set header label
        self.header = QLabel()
        self._set_header()
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setFixedHeight(30)
        self.header.mousePressEvent = self.toggle
        self.header_layout.addWidget(self.header)

        # Set removal button
        self.remove_button = QPushButton("-", self)
        self.remove_button.setFixedWidth(30)
        self.remove_button.clicked.connect(self.emit_remove_signal)
        self.header_layout.addWidget(self.remove_button)

    def _init_content(self):
        # Content layout
        self.content_layout = QVBoxLayout()
        self.content_container = QFrame()
        self.content_container.setLayout(self.content_layout)
        self.content_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.main_layout.addWidget(self.content_container)
        
        # Inputs layout
        self.inputs_layout = QVBoxLayout()
        self.content_layout.addLayout(self.inputs_layout)

        # Set OK button
        self.confirm_button = QPushButton("OK", self)
        self.confirm_button.clicked.connect(self.emit_data_signal)
        self.confirm_button.setEnabled(False)
        self.content_layout.addWidget(self.confirm_button)

        # Initially collapse ShaftSubsection widget
        self.expanded = True
        self.toggle(None)
    
    def _set_header(self):
        self.header.setText(f'{self.subsection_number + 1}.')
    
    def _check_if_all_inputs_provided(self):
        self.confirm_button.setEnabled(all(input.text() != '' for input in self.inputs.values()) and all(literal_eval(input.text()) != 0 for input in self.inputs.values()))
    
    def _check_if_meets_limits(self, input=None):
        input = self.sender() if input == None else input
        attribute = next((key for key, value in self.inputs.items() if value == input), None)

        if attribute:
            min = self.limits[attribute]['min']
            max = self.limits[attribute]['max']
            value = float(input.text()) if input.text() else None

            input.setPlaceholderText(f'{format_input(min)}-{format_input(max)}')
            if value is not None and min <= value <= max:
                input.setText(f'{format_input(value)}')
            else:
                input.clear()

    def set_attributes(self, attributes):
        # Set data entries
        for attribute in attributes:
            id = attribute[0]
            symbol = attribute[1]

            attribute_row, input = create_data_input_row(symbol)
            self.inputs_layout.addLayout(attribute_row)

            self.add_input(id, input)
    
    def add_input(self, id, input):
        input.textChanged.connect(self._check_if_all_inputs_provided)
        input.editingFinished.connect(self._check_if_meets_limits)
        self.inputs[id] = input

    def get_attributes(self):
        return {key: literal_eval(input.text()) for key, input in self.inputs.items()}
    
    def update_subsection_name(self, new_number):
        self.subsection_number = new_number
        self._set_header()
    
    def set_limits(self, limits):
        for attribute, attribute_limits in limits.items():
            if attribute in self.inputs.keys():
                self.limits[attribute] = {}
                for limit, value in attribute_limits.items():
                    self.limits[attribute][limit] = value
                self._check_if_meets_limits(self.inputs[attribute])

    def toggle(self, event):
        # Collapse or expand contents of section
        self.expanded = not self.expanded
        self.content_container.setVisible(self.expanded)

        self.adjustSize()
        self.updateGeometry()

    def emit_data_signal(self):
        self.subsection_data_signal.emit(self.get_attributes())
    
    def emit_remove_signal(self):
        self.remove_subsection_signal.emit(self.subsection_number)
