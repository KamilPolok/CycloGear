from ast import literal_eval

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

from config import resource_path

from .CommonFunctions import create_data_input_row, format_input

class CustomFrame(QFrame):
    def __init__(self):
        super().__init__()
        self._default_style = "QFrame { background-color: #c1c9c9; }"
        self._on_hover_style = "QFrame { background-color: #9aa1a1; }"
        self.setStyleSheet(self._default_style)

class HoverButton(QPushButton):
    def __init__(self, parent: QFrame):
        super().__init__(parent)

    def enterEvent(self, event):
        self.parent().setStyleSheet(self.parent()._on_hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.parent().setStyleSheet(self.parent()._default_style)
        super().leaveEvent(event)

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
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self._init_header()
        self._init_content()

    def _init_header(self):
        # Set header layout
        header = CustomFrame()
        self.header_height = 25
        header.setFixedHeight(self.header_height)  # Set the height to 30 pixels
        self._main_layout.addWidget(header)

        self._header_layout = QHBoxLayout()
        self._header_layout.setContentsMargins(0, 0, 0, 0)
        self._header_layout.setSpacing(0)
        self._header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.setLayout(self._header_layout)

        # Set toggle section button
        self._toggle_section_button = HoverButton(header)
        self._toggle_section_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._toggle_section_button.setStyleSheet("""                                                  
            QPushButton {
                background-color: transparent;
                text-align: left;
                font-size: 10pt;
                font-weight: 600;                                
                padding-left: 10px
            }
        """)

        self._set_name()
        self._toggle_section_button.clicked.connect(self.toggle_content)
        self._header_layout.addWidget(self._toggle_section_button)

        # Set removal button
        self.remove_button = QPushButton()
        button_size = self.header_height
        icon_size = self.header_height * 0.9
        self.remove_button.setFixedSize(button_size, button_size)
        self.remove_button.setIconSize(QSize(icon_size, icon_size))
        self.remove_button.setIcon(QIcon(resource_path('icons//remove_btn.png')))
        self.remove_button.setStyleSheet("""                         
            QPushButton {
                background-color: transparent;
                color: black;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #9aa1a1;
                border: 1px solid #9aa1a1;
            }
            QPushButton:pressed {
                background-color: #5a6161;
                border: 1px solid #5a6161;
            }
        """)
        self.remove_button.clicked.connect(self.emit_remove_signal)
        self._header_layout.addWidget(self.remove_button)

    def _init_content(self):
        # _content layout
        self._content = QFrame()
        self._content_layout = QVBoxLayout()
        self._content.setLayout(self._content_layout)
        self._content_layout.setContentsMargins(5, 0, 0, 0)
        self._main_layout.addWidget(self._content)
        
        # Inputs layout
        self._inputs_layout = QVBoxLayout()
        self._content_layout.addLayout(self._inputs_layout)

        # Set OK button
        self._confirm_button = QPushButton("OK", self)
        self._confirm_button.clicked.connect(self.emit_data_signal)
        self._confirm_button.setEnabled(False)
        self._content_layout.addWidget(self._confirm_button)

    
    def _set_name(self):
        self._toggle_section_button.setText(f'Stopień {self.subsection_number + 1}')
    
    def _check_if_all_inputs_provided(self):
        self._confirm_button.setEnabled(all(input.text() != '' for input in self.inputs.values()) and all(literal_eval(input.text()) != 0 for input in self.inputs.values()))
    
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
            self._inputs_layout.addLayout(attribute_row)

            self.add_input(id, input)
    
    def add_input(self, id, input):
        input.textChanged.connect(self._check_if_all_inputs_provided)
        input.editingFinished.connect(self._check_if_meets_limits)
        self.inputs[id] = input

    def get_attributes(self):
        return {key: literal_eval(input.text()) for key, input in self.inputs.items()}
    
    def update_subsection_name(self, new_number):
        self.subsection_number = new_number
        self._set_name()
    
    def set_limits(self, limits):
        for attribute, attribute_limits in limits.items():
            if attribute in self.inputs.keys():
                self.limits[attribute] = {}
                for limit, value in attribute_limits.items():
                    self.limits[attribute][limit] = value
                self._check_if_meets_limits(self.inputs[attribute])

    def toggle_content(self, event):
        self._content.setVisible(not self._content.isVisible())

        self.adjustSize()
        self.updateGeometry()

    def emit_data_signal(self):
        self.subsection_data_signal.emit(self.get_attributes())
    
    def emit_remove_signal(self):
        self.remove_subsection_signal.emit(self.subsection_number)
