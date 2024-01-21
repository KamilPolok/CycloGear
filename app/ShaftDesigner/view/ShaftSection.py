from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QSizePolicy

from PyQt6.QtCore import pyqtSignal

from .ShaftSubsection import ShaftSubsection

class ShaftSection(QWidget):
    subsection_data_signal = pyqtSignal(dict)
    add_subsection_signal = pyqtSignal()
    remove_subsection_plot_signal = pyqtSignal(str, int)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.subsections = []
        self.subsection_count = 0

        self._init_ui()

    def _init_ui(self):
        # Main layout
        self.layout = QVBoxLayout(self)

        self._init_header()
        self._init_subsections()

        # Initially collapse ShaftSection widget
        self.expanded = True
        self.toggle(None)
    
    def _init_header(self):
        # Header layout
        self.header_layout = QHBoxLayout()

        # Set header
        self.header = QLabel(self.name)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setFixedHeight(30)
        self.header.mousePressEvent = self.toggle
        self.header_layout.addWidget(self.header)

        # Set add subsection button
        self.add_subsection_button = QPushButton("+", self)
        self.add_subsection_button.clicked.connect(self.add_subsection)
        self.add_subsection_button.setFixedWidth(30)
        self.header_layout.addWidget(self.add_subsection_button)

        # Add header layout to main layout
        self.layout.addLayout(self.header_layout)
    
    def _init_subsections(self):
        # Set subsections layout
        self.subsections_layout = QVBoxLayout()
        self.subsections_container = QFrame()
        self.subsections_container.setLayout(self.subsections_layout)
        self.layout.addWidget(self.subsections_container)

        # Add one subsection
        self.add_subsection()

    def add_subsection(self):
        subsection = ShaftSubsection(self.name, self.subsection_count, self)
        subsection.subsection_data_signal.connect(self.handle_subsection_data)
        subsection.remove_subsection_signal.connect(self.remove_subsection)
        self.subsections.append(subsection)
        self.subsections_layout.addWidget(subsection)
        self.subsection_count += 1

    def remove_subsection(self, subsection_number):
        # Find and remove the specific subsection
        if len(self.subsections) > 0:
            subsection_to_remove = next((s for s in self.subsections if s.subsection_number == subsection_number), None)
            if subsection_to_remove:
                self.subsections_layout.removeWidget(subsection_to_remove)
                subsection_to_remove.deleteLater()
                self.subsections = [s for s in self.subsections if s != subsection_to_remove]
        
            # Update the numbers and names of the remaining subsections
                for i, subsection in enumerate(self.subsections):
                    subsection.update_subsection_name(i)

            # Update the subsection count
            self.subsection_count = len(self.subsections)
        
        self.remove_subsection_plot_signal.emit(self.name, subsection_number)
    
    def toggle(self, event):
        # Expand or collapse the widget
        self.expanded = not self.expanded
        self.subsections_container.setVisible(self.expanded)
        self.add_subsection_button.setVisible(self.expanded)

    def handle_subsection_data(self, data):
        self.subsection_data_signal.emit(data)
