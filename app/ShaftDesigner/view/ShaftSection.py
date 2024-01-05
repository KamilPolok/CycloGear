from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QSizePolicy

from PyQt6.QtCore import pyqtSignal

from .ShaftSubsection import ShaftSubsection

class ShaftSection(QWidget):
    subsection_data_signal = pyqtSignal(dict)
    add_subsection_signal = pyqtSignal()
    remove_subsection_plot_signal = pyqtSignal(str, int)

    def __init__(self, name):
        super().__init__()
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
        subsection = ShaftSubsection(self.name, self.subsection_count, self)
        subsection.subsection_data_signal.connect(self.handle_subsection_data)
        subsection.remove_subsection_signal.connect(self.remove_subsection)
        self.subsections.append(subsection)
        self.subsections_layout.addWidget(subsection)
        self.set_remove_subsection_buttons_visibile()
        self.set_add_subsection_button_enabled(False)
        self.subsection_count += 1
        if self.subsection_count > 0:
            self.add_subsection_signal.emit()
    
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
            
            # Update the visibility of the remove buttons
            self.set_remove_subsection_buttons_visibile()
        
        self.remove_subsection_plot_signal.emit(self.name, subsection_number)
    
    def set_remove_subsection_buttons_visibile(self):
        # Show the remove button only if there are more than one subsections
        single_subsection = len(self.subsections) == 1
        for subsection in self.subsections:
            subsection.remove_button.setVisible(not single_subsection)
    
    def set_add_subsection_button_visibile(self, visible):
        self.add_subsection_button.setVisible(visible)

    def set_add_subsection_button_enabled(self, enabled):
        self.add_subsection_button.setEnabled(enabled)
    
    def toggle(self, event):
        # Toggle the visibility of the subsections
        self.expanded = not self.expanded
        for i in range(self.subsections_layout.count()): 
            widget = self.subsections_layout.itemAt(i).widget()
            if widget is not None:
                widget.setVisible(self.expanded)
    
    def set_limits(self, limits):
        for subsection_number, attributes in limits.items():
            for attribute, attribute_limits in attributes.items():
                self.subsections[subsection_number].set_limits(attribute, attribute_limits)

    def handle_subsection_data(self, data):
        self.subsection_data_signal.emit(data)
