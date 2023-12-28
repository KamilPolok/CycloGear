from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QSizePolicy

from PyQt6.QtCore import pyqtSignal

from .ShaftSubsection import ShaftSubsection


class ShaftSection(QWidget):
    subsection_data_signal = pyqtSignal(dict)
    subsection_removed_signal = pyqtSignal(str, int)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.subsections = []
        self.subsection_count = 0
        self._init_ui()

    def _init_ui(self):
        # Set layout
        self.layout = QVBoxLayout(self)

        # Set header
        self.header = QLabel(self.name)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setFixedHeight(30)
        self.header.mousePressEvent = self.toggle
        self.layout.addWidget(self.header)

        # Set subsections layout
        self.subsections_layout = QVBoxLayout()
        self.layout.addLayout(self.subsections_layout)

        # Set add subsection button
        self.add_subsection_button = QPushButton("+", self)
        self.add_subsection_button.clicked.connect(self.add_subsection)
        self.layout.addWidget(self.add_subsection_button)

        # Initially add one subsection
        self.add_subsection()

        # Initially collapse ShaftSection widget
        self.expanded = True
        self.toggle(None)

    def add_subsection(self):
        self.subsection_count += 1
        subsection = ShaftSubsection(self.name, self.subsection_count, self)
        subsection.subsection_data_signal.connect(self.handle_subsection_data)
        subsection.remove_subsection_signal.connect(self.remove_subsection)
        self.subsections.append(subsection)
        self.subsections_layout.addWidget(subsection)
        self.update_remove_buttons_visibility()
    
    def remove_subsection(self, subsection_number):
        # Find and remove the specific subsection
        if len(self.subsections) > 1:
            subsection_to_remove = next((s for s in self.subsections if s.subsection_number == subsection_number), None)
            if subsection_to_remove:
                self.subsections_layout.removeWidget(subsection_to_remove)
                subsection_to_remove.deleteLater()
                self.subsections = [s for s in self.subsections if s != subsection_to_remove]
        
            # Update the numbers and names of the remaining subsections
                for i, subsection in enumerate(self.subsections, start=1):
                    subsection.update_subsection_name(i)

            # Update the subsection count
            self.subsection_count = len(self.subsections)
            
            # Update the visibility of the remove buttons
            self.update_remove_buttons_visibility()
        
        self.subsection_removed_signal.emit(self.name, subsection_number)
    
    def update_remove_buttons_visibility(self):
        # Show the remove button only if there are more than one subsections
        single_subsection = len(self.subsections) == 1
        for subsection in self.subsections:
            subsection.remove_button.setVisible(not single_subsection)
    
    def toggle(self, event):
        # Toggle the visibility of the subsections
        self.expanded = not self.expanded
        for i in range(self.subsections_layout.count()): 
            widget = self.subsections_layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(self.expanded)
    
    def set_add_subsection_button_visibility(self, visible):
        self.add_subsection_button.setVisible(visible)
    
    def handle_subsection_data(self, data):
        self.subsection_data_signal.emit(data)