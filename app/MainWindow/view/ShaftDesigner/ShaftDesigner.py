from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QStyle,
                             QVBoxLayout, QWidget, QScrollArea)

from .Chart import Chart
from .ShaftSection import ShaftSection

class ShaftDesigner(QMainWindow):
    """
    A class representing chart and interface to design the shaft

    This class is responsible for comunication between chart and
    other components of the application and also for implementing
    the GUI for interactive shaft design
    """
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        # Set window parameters
        self.setWindowTitle("Wał Wejściowy")
        self.resize(800,500)

        # Set layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        self._init_chart()

    def _init_chart(self):
        # Add Chart
        self.chart = Chart()
        self.centralWidget().layout().addWidget(self.chart)
    
    def init_sidebar(self, section_names):
        # Set layout for sidebar and toggle button
        self.sidebar_section_layout  = QHBoxLayout()

        # Set sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar.setFixedWidth(200)  # Set the fixed width for the sidebar

        # Set contents of the sidebar
        self.sections = {}
        for name in section_names:
            section = ShaftSection(name, self)
            self.sections[name] = section
            # Initially disable all sections except the 'Mimośrody' one:
            if name != 'Mimośrody':
                section.setEnabled(False)
            self.sidebar_layout.addWidget(section)
        
        # Disable option to add new subsections for sections below
        self.sections['Mimośrody'].set_add_subsection_button_visibility(False)
        self.sections['Pomiędzy mimośrodami'].set_add_subsection_button_visibility(False)

        # Disable changing the default values of data entries in certain subsections below
        self.sections['Pomiędzy mimośrodami'].subsections[0].set_read_only('l')

        # Add a spacer item at the end of the sidebar layout - keeps the contents alignet to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.sidebar_layout .addSpacerItem(spacer)

        # Set a scroll area for the sidebar - make the sidebar scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sidebar)
        self.scroll_area.setFixedWidth(220)  # Slightly larger to accommodate scrollbar

        # Set sidebar toggle button
        self.toggle_button_layout = QVBoxLayout()

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)  # Example icon
        self.toggle_button = QPushButton(icon, '')
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: none;
                border: none;
            }                               
        """)
        self.toggle_button.setFixedWidth(50)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.toggle_button_layout.addWidget(self.toggle_button)
        self.toggle_button_layout.addStretch(1)

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addLayout(self.toggle_button_layout)

    def toggle_sidebar(self):
        self.scroll_area.setVisible(not self.scroll_area.isVisible())

class ShaftDesignerController:
    def __init__(self, view):
        self._shaft_designer = view

        # Set shaft sections names
        self.section_names = ['Mimośrody', 'Przed mimośrodami', 'Pomiędzy mimośrodami', 'Za mimośrodami']

        # Prepare dict storing shaft sections attributes
        self.shaft_sections = {}

        self._startup()
    
    def _connect_signals_and_slots(self):
        for section in self._shaft_designer.sections.values():
            section.subsection_data_signal.connect(self._calculate_shaft_sections)
            section.remove_subsection_plot_signal.connect(self._remove_subsection_plot)
    
    def _startup(self):
        self._init_ui()
        self._connect_signals_and_slots()

    def _init_ui(self):
        self._shaft_designer.init_sidebar(self.section_names)
    
    def _save_shaft_sections_attributes(self, shaft_subsection_attributes):
        if shaft_subsection_attributes:
            for section_name, section in shaft_subsection_attributes.items():
                if section_name in self.shaft_sections:
                    self.shaft_sections[section_name].update(section)
                else:
                    self.shaft_sections[section_name] = section

    def _calculate_shaft_sections(self, shaft_subsection_attributes = None):
        # Save subsection attrbutes
        if shaft_subsection_attributes:
            self._save_shaft_sections_attributes(shaft_subsection_attributes)

        # Prepare dict storing shaft subsections drawing attributes
        self.shaft_sections_plots_attributes = {section_name: {} for section_name in ['Mimośrody1', 'Mimośrody2', 'Przed mimośrodami', 'Pomiędzy mimośrodami', 'Za mimośrodami']}
        
        # Calculate shaft section attributes
        if 'Mimośrody' in self.shaft_sections:
            self._calculate_eccentrics_section()
        if 'Przed mimośrodami' in self.shaft_sections:
            self._calculate_section_before_eccentricities()
        if 'Pomiędzy mimośrodami' in self.shaft_sections:
            self._calculate_section_between_eccentricities()
        if 'Za mimośrodami' in self.shaft_sections:
            self._calculate_section_after_eccentricities()

        # Draw shaft
        self._shaft_designer.chart.draw_shaft(self.shaft_sections_plots_attributes)
        
        # If 'Mimośrody' section is calculated, enable other sections
        if 'Mimośrody' in self.shaft_sections:
            for section in self._shaft_designer.sections.values():
                section.setEnabled(True)
    
    def _calculate_eccentrics_section(self):
        section = 'Mimośrody'
        length = self.shaft_sections[section][0]['l']
        diameter = self.shaft_sections[section][0]['d']

        eccentric1_position = self._shaft_attributes['L1']
        offset = self._shaft_attributes['e']

        # If length of the eccentrics changed, calculate and redraw the new shaft coordinates
        if length != self._shaft_attributes['B']:
            length_between = self._shaft_attributes['x']
            eccentric2_position = eccentric1_position + length + length_between

            self._shaft_attributes['L2'] = eccentric2_position
            self._shaft_attributes['B'] = length

            # Redraw shaft coordinates
            self._shaft_designer.chart._draw_shaft_coordinates()
        else:
            eccentric2_position = self._shaft_attributes['L2']

        eccentric1_start_z = eccentric1_position - length / 2
        eccentric1_start_y = offset - diameter / 2

        eccentric2_start_z = eccentric2_position - length / 2
        eccentric2_start_y = -offset - diameter / 2

        self.shaft_sections_plots_attributes[section + '1'][0] = [(eccentric1_start_z, eccentric1_start_y), length, diameter]
        self.shaft_sections_plots_attributes[section + '2'][0] = [(eccentric2_start_z, eccentric2_start_y), length, diameter]

    def _calculate_section_between_eccentricities(self):
        # Draw the shaft section between the eccentrics
        section ='Pomiędzy mimośrodami'
        length = self.shaft_sections[section][0]['l']
        diameter = self.shaft_sections[section][0]['d']
        start_z = self._shaft_attributes['L1'] + self.shaft_sections['Mimośrody'][0]['l'] / 2
        start_y = -diameter / 2

        self.shaft_sections_plots_attributes[section][0] = [(start_z, start_y), length, diameter]

    def _calculate_section_before_eccentricities(self):
        # Draw the shaft section before the first eccentric
        section ='Przed mimośrodami'

        start_z = self._shaft_attributes['L1'] - self.shaft_sections['Mimośrody'][0]['l'] / 2

        for subsection_number, subsection_data in self.shaft_sections[section].items():
            length = subsection_data['l']
            diameter = subsection_data['d']
            start_z -= length
            start_y = -diameter / 2

            self.shaft_sections_plots_attributes[section][subsection_number] = [(start_z, start_y), length, diameter]
        
    def _calculate_section_after_eccentricities(self):
        # Draw the shaft section after the second eccentric
        section ='Za mimośrodami'
        start_z = self._shaft_attributes['L2'] + self.shaft_sections['Mimośrody'][0]['l'] / 2

        for subsection_number, subsection_data in self.shaft_sections[section].items():
            length = subsection_data['l']
            diameter = subsection_data['d']
            start_y = -diameter / 2
            
            self.shaft_sections_plots_attributes[section][subsection_number] = [(start_z, start_y), length, diameter]
            
            start_z += length  # Update start_z for the next subsection
    
    def _remove_subsection_plot(self, section_name, subsection_number):
        # Remove the subsection from shaft sections attributes
        if section_name in self.shaft_sections and subsection_number in self.shaft_sections[section_name]:
            del self.shaft_sections[section_name][subsection_number]

            # Adjust the numbering of the remaining subsections
            new_subsections = {}
            for num, data in enumerate(self.shaft_sections[section_name].values()):
                new_subsections[num] = data
            self.shaft_sections[section_name] = new_subsections

            # Recalculate and redraw shaft sections
            self._calculate_shaft_sections()

    def set_initial_data(self, data):
        # Set shaft attributes
        self._shaft_attributes = data

        # Set initial shaft sections attributes
        self._initial_shaft_sections_attributes = { 
            self.section_names[0]: {'l': data['B'], 'd': data['de']},
            self.section_names[1]: {'l': None, 'd': data['ds']},
            self.section_names[2]: {'l': data['x'], 'd': data['ds']},
            self.section_names[3]: {'l': None, 'd': data['ds']},
        }

        # Set initial shaft sections input values to shaft initial attributes
        for section_name, section in self._shaft_designer.sections.items():
            for subsection in section.subsections:
                subsection.set_attributes(self._initial_shaft_sections_attributes[section_name])

        # Init plots
        self._shaft_designer.chart.init_plots(data)
        # Redraw shaft section if anything is already drawn on the chart
        if self.shaft_sections:
            self._calculate_shaft_sections()
