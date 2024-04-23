from ast import literal_eval

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

from config import resource_path

from .CommonFunctions import create_data_input_row, format_input

class CustomFrame(QFrame):
    def __init__(self):
        super().__init__()
        self._default_style = "QFrame { background-color: #8ad6cc; border-radius: 5px;}"
        self._on_hover_style = "QFrame { background-color: #66beb2; border-radius: 5px;}"
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

    def __init__(self, subsection_name, subsection_number, parent=None):
        super().__init__(parent)
        self.subsection_name = subsection_name
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

        # Set initial view
        self._content.setVisible(False)
        self._confirm_button.setEnabled(False)
        self._confirm_button.setVisible(False)

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

        # Set confirmation button
        self._confirm_button = QPushButton()
        button_size = self.header_height
        icon_size = self.header_height * 0.9
        self._confirm_button.setFixedSize(button_size, button_size)
        self._confirm_button.setIconSize(QSize(icon_size, icon_size))
        self._confirm_button.setIcon(QIcon(resource_path('icons//confirm.png')))
        self._confirm_button.setToolTip('Zatwierdź')
        self._confirm_button.setStyleSheet("""                         
            QPushButton {
                background-color: transparent;
                color: black;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #66beb2;
                border: 1px solid #66beb2;
            }
            QPushButton:pressed {
                background-color: #51988e;
                border: 1px solid #51988e;
            }
        """)
        self._confirm_button.clicked.connect(self.emit_data_signal)
        self._header_layout.addWidget(self._confirm_button)

        # Set removal button
        self.remove_button = QPushButton()
        button_size = self.header_height
        icon_size = self.header_height * 0.9
        self.remove_button.setFixedSize(button_size, button_size)
        self.remove_button.setIconSize(QSize(icon_size, icon_size))
        self.remove_button.setIcon(QIcon(resource_path('icons//remove_btn.png')))
        self.remove_button.setToolTip('Usuń')
        self.remove_button.setStyleSheet("""                         
            QPushButton {
                background-color: transparent;
                color: black;
                border: 1px solid transparent;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #66beb2;
                border: 1px solid #66beb2;
            }
            QPushButton:pressed {
                background-color: #51988e;
                border: 1px solid #51988e;
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
    
    def _set_name(self):
        self._toggle_section_button.setText(f'{self.subsection_name} {self.subsection_number + 1}')
    
    def _check_if_all_inputs_provided(self):
        self._confirm_button.setEnabled(all(input.text() != '' for input in self.inputs.values()) and all(literal_eval(input.text()) != 0 for input in self.inputs.values()))
    
    def _check_if_meets_limits(self):
        input = self.sender()
        attribute = next((key for key, value in self.inputs.items() if value == input), None)

        if attribute:
            min = self.limits[attribute]['min']
            max = self.limits[attribute]['max']
            value = float(input.text()) if input.text() else None

            if value is not None and value != 0:
                if min <= value <= max:
                    input.setText(f'{format_input(value)}')
                elif min > value:
                    input.setText(f'{format_input(min)}')
                elif max < value:
                    input.setText(f'{format_input(max)}')
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
                min = attribute_limits['min']
                max = attribute_limits['max']
                self.limits[attribute]['min'] = min
                self.limits[attribute]['max'] = max
                self.inputs[attribute].setPlaceholderText(f'{format_input(min)}-{format_input(max)}')
    
    def set_values(self, values):
        for attribute, value in values.items():
            if attribute in self.inputs.keys():
                if value is not None and value !=0:
                    self.inputs[attribute].setText(f'{format_input(value)}')
                else:
                     self.inputs[attribute].clear()

    def toggle_content(self, event):
        self._content.setVisible(not self._content.isVisible())
        self._confirm_button.setVisible(not self._confirm_button.isVisible())

        self.adjustSize()
        self.updateGeometry()

    def emit_data_signal(self):
        self.subsection_data_signal.emit(self.get_attributes())
    
    def emit_remove_signal(self):
        self.remove_subsection_signal.emit(self.subsection_number)
