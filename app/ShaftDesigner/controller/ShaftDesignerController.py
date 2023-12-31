from ShaftDesigner.view.Chart import Chart
from ShaftDesigner.view.ShaftSection import ShaftSection

class ShaftDesignerController:
    def __init__(self, view):
        self._shaft_designer = view

        # Set shaft sections names
        self.section_names = ['Mimośrody', 'Przed mimośrodami', 'Pomiędzy mimośrodami', 'Za mimośrodami']

        # Prepare dict storing shaft sections attributes
        self.shaft_sections = {}

        # Prepare dict storing sidebar sections
        self._sidebar_sections = {}

        self._init_ui()
        self._connect_signals_and_slots()
    
    def _connect_signals_and_slots(self):
        for section in self._sidebar_sections.values():
            section.subsection_data_signal.connect(self._calculate_shaft_sections)
            section.remove_subsection_plot_signal.connect(self._remove_subsection_plot)

    def _init_ui(self):
        # Set an instance of chart
        self._chart = Chart()
        self._shaft_designer.init_chart(self._chart)

        # Set instances of sidebar sections
        for name in self.section_names:
            section = ShaftSection(name)
            self._sidebar_sections[name] = section
        
        # Initially disable all sections except the 'Mimośrody' one:
        for section_name, section in self._sidebar_sections.items():
            if section_name != 'Mimośrody':
                section.setEnabled(False)

        # Disable option to add new subsections for sections below
        self._sidebar_sections['Mimośrody'].set_add_subsection_button_visibility(False)
        self._sidebar_sections['Pomiędzy mimośrodami'].set_add_subsection_button_visibility(False)

        # Disable changing the default values of data entries in certain subsections below
        self._sidebar_sections['Pomiędzy mimośrodami'].subsections[0].set_read_only('l')

        self._shaft_designer.init_sidebar(self._sidebar_sections)
    
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
        self._chart.draw_shaft(self.shaft_sections_plots_attributes)
        
        # If 'Mimośrody' section is calculated, enable other sections in sidebar
        if 'Mimośrody' in self.shaft_sections:
            for section in self._sidebar_sections.values():
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
            self._chart._draw_shaft_coordinates()
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
        for section_name, section in self._sidebar_sections.items():
            for subsection in section.subsections:
                subsection.set_attributes(self._initial_shaft_sections_attributes[section_name])

        # Init plots
        self._chart.init_plots(data)
        # Redraw shaft section if anything is already drawn on the chart
        if self.shaft_sections:
            self._calculate_shaft_sections()
