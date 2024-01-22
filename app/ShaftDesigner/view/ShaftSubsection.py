from ast import literal_eval

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from .CommonFunctions import create_data_input_row

class ShaftSubsection(QWidget):
    check_if_inputs_provided_signal = pyqtSignal()
    subsection_data_signal = pyqtSignal(dict)
    remove_subsection_signal = pyqtSignal(int)

    def __init__(self, section_name, subsection_number, parent=None):
        super().__init__(parent)
        self.section_name = section_name
        self.subsection_number = subsection_number
        self.expanded = False
        self.inputs = {}

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
            self.check_if_inputs_provided_signal.emit()

    def set_attributes(self, attributes):
        # Set data entries
        for attribute in attributes:
            symbol = attribute[0]
            label = attribute[1]

            attribute_row, input = create_data_input_row(symbol, label)
            self.inputs_layout.addLayout(attribute_row)
            
            input.textChanged.connect(self._check_if_all_inputs_provided)
            self.inputs[symbol] = input

    def get_attributes(self):
        return {key: literal_eval(input.text()) for key, input in self.inputs.items()}
    
    def update_subsection_name(self, new_number):
        self.subsection_number = new_number
        self._set_header()
    
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
