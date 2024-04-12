
from abc import ABC, ABCMeta, abstractmethod
from ast import literal_eval

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QSizePolicy 
from PyQt6.QtGui import QIcon

from .CommonFunctions import create_data_input_row
from .ShaftSubsection import ShaftSubsection

from config import resource_path

class CustomFrame(QFrame):
    def __init__(self):
        super().__init__()

        self._default_style = "QFrame { background-color: #c1c9c9;}"
        self._on_hover_style = "QFrame { background-color: #9aa1a1;}"
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

class ABCQWidgetMeta(ABCMeta, type(QWidget)):
    pass
class Section(QWidget, metaclass=ABCQWidgetMeta):
    subsection_data_signal = pyqtSignal(tuple)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self._name = name
        self.subsections = []
        self.subsection_count = 0

        self._init_ui()

    def _init_ui(self):
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        
        self._init_header()
        self._init_content()
    
    def _init_header(self):
        # Set header layout
        header = CustomFrame()
        self._header_height = 25
        header.setFixedHeight(self._header_height)  # Set the height to 30 pixels
        self._main_layout.addWidget(header)

        self._header_layout = QHBoxLayout()
        self._header_layout.setContentsMargins(0, 0, 0, 0)
        self._header_layout.setSpacing(0)
        self._header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.setLayout(self._header_layout)

        # Set toggle section button
        self.toggle_section_button = HoverButton(header)
        self.toggle_section_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.toggle_section_button.setStyleSheet("""                                                  
            QPushButton {
                background-color: transparent;
                text-align: left;
                font-size: 10pt;
                font-weight: 600;                                
                padding-left: 10px
            }
        """)
        self.toggle_section_button.setText(self._name)
        self.toggle_section_button.clicked.connect(self.toggle_content)
        self._header_layout.addWidget(self.toggle_section_button)
    
    def _init_content(self):
        # Set content layout
        self._content = QFrame()
        self._content_layout = QVBoxLayout()
        self._content_layout.setContentsMargins(5, 0, 0, 0)
        self._content.setLayout(self._content_layout)

        self._main_layout.addWidget(self._content)

        self._content.setVisible(False)

    def toggle_content(self, event):
        '''
        Toggle the visibility of the content section
        '''
        self._content.setVisible(not self._content.isVisible())

    @abstractmethod
    def handle_subsection_data(self, data):
        pass

class ShaftSection(Section):
    add_subsection_signal = pyqtSignal()
    remove_subsection_plot_signal = pyqtSignal(str, int)

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self._subsection_name = 'Stopień'
    
    def _init_header(self):
        super()._init_header()
        # Set add subsection button
        self._add_subsection_button = QPushButton()
        button_size = self._header_height
        icon_size = self._header_height * 0.9
        self._add_subsection_button.setFixedSize(button_size, button_size)
        self._add_subsection_button.setIconSize(QSize(icon_size, icon_size))
        self._add_subsection_button.setIcon(QIcon(resource_path('icons//add_btn.png')))
        self._add_subsection_button.setStyleSheet("""                         
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
        
        self._add_subsection_button.clicked.connect(self.add_subsection)
        self._header_layout.addWidget(self._add_subsection_button)

        self._add_subsection_button.setVisible(False)

    def add_subsection(self):
        subsection = ShaftSubsection(self._subsection_name, self.subsection_count, self)
        subsection.set_attributes([('d', 'Ø'), ('l', 'L')])
        subsection.subsection_data_signal.connect(self.handle_subsection_data)
        subsection.remove_subsection_signal.connect(self.remove_subsection)
        self.subsections.append(subsection)
        self._content_layout.addWidget(subsection)
        self.subsection_count += 1
        self.set_add_subsection_button_enabled(False)
        self.add_subsection_signal.emit()

    def remove_subsection(self, subsection_number):
        # Find and remove the specific subsection
        subsection_to_remove = self.sender()
        self._content_layout.removeWidget(subsection_to_remove)
        subsection_to_remove.deleteLater()
        self.subsections = [s for s in self.subsections if s != subsection_to_remove]
    
        # Update the numbers and names of the remaining subsections
        for i, subsection in enumerate(self.subsections):
            subsection.update_subsection_name(i)

        # Update the subsection count
        self.subsection_count -= 1
        
        self.remove_subsection_plot_signal.emit(self._name, subsection_number)

    def set_limits(self, limits):
        for subsection_number, attributes in limits.items():
            self.subsections[subsection_number].set_limits(attributes)
    
    def set_add_subsection_button_enabled(self, enabled):
        self._add_subsection_button.setEnabled(enabled)
    
    def toggle_content(self, event):
        super().toggle_content(event)
        self._add_subsection_button.setVisible(not self._add_subsection_button.isVisible())

    def handle_subsection_data(self, subsection_data):
        subsection = self.sender()
        common_section_data = None
        data = (self._name, subsection.subsection_number, subsection_data, common_section_data)
        self.subsection_data_signal.emit(data)

class EccentricsSection(Section):
    remove_subsection_plot_signal = pyqtSignal(str, int)

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.subsection_name = 'Wykorbienie'

    def _init_content(self):
        super()._init_content()

        # Set data entries
        self.inputs = {}
        
        attribute, symbol = ('d', 'Ø')
        attribute_row, input = create_data_input_row(symbol)
        self._content_layout.addLayout(attribute_row)
        
        self.inputs[attribute] = input

    def set_subsections_number(self, sections_number):
        if self.subsection_count < sections_number:
            # Add subsections
            for _ in range(self.subsection_count, sections_number):
                subsection = ShaftSubsection(self.subsection_name, self.subsection_count, self)
                subsection.set_attributes([('l', 'L')])
                for attribute, input in self.inputs.items():
                    subsection.add_input(attribute, input)
                subsection.remove_button.hide()
                subsection.subsection_data_signal.connect(self.handle_subsection_data)
                self.subsections.append(subsection)
                self._content_layout.addWidget(subsection)
                self.subsection_count += 1
        elif self.subsection_count > sections_number:
            # Remove subsections
            while self.subsection_count > sections_number:
                last_subsection_number = self.subsection_count-1
                self.remove_subsection(last_subsection_number)

    def remove_subsection(self, subsection_number):
        # Find and remove the specific subsection
        subsection_to_remove = self.subsections[subsection_number]
        self._content_layout.removeWidget(subsection_to_remove)
        subsection_to_remove.deleteLater()
        self.subsections = [s for s in self.subsections if s != subsection_to_remove]
    
        # Update the numbers and names of the remaining subsections
        for i, subsection in enumerate(self.subsections):
            subsection.update_subsection_name(i)

        # Update the subsection count
        self.subsection_count -= 1
        
        self.remove_subsection_plot_signal.emit(self._name, subsection_number)

    def set_limits(self, limits):
        for subsection_number, attributes in limits.items():
            self.subsections[subsection_number].set_limits(attributes)

    def handle_subsection_data(self, subsection_data):
        subsection = self.sender()
        common_section_data = {key: literal_eval(input.text()) for key, input in self.inputs.items()}
        data = (self._name, subsection.subsection_number, subsection_data, common_section_data)
        self.subsection_data_signal.emit(data)
