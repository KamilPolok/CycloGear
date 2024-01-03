class ShaftCalculator:
    def __init__(self):
        self.shaft_sections = {}

    def set_data(self, shaft_attributes):
        self._shaft_attributes = shaft_attributes

    def _save_shaft_sections_attributes(self, shaft_subsection_attributes):
        if shaft_subsection_attributes:
            for section_name, section in shaft_subsection_attributes.items():
                if section_name in self.shaft_sections:
                    self.shaft_sections[section_name].update(section)
                else:
                    self.shaft_sections[section_name] = section
        
    def calculate_shaft_sections(self, shaft_subsection_attributes = None):
        # Save subsection attrbutes
        if shaft_subsection_attributes:
            self._save_shaft_sections_attributes(shaft_subsection_attributes)

        # Prepare dict storing shaft subsections drawing attributes
        self.shaft_sections_plots_attributes = {section_name: {} for section_name in ['Mimośrody1', 'Mimośrody2', 'Przed mimośrodami', 'Pomiędzy mimośrodami', 'Za mimośrodami']}

        self.is_eccentrics_length_changed = False
        
        # Calculate shaft section attributes
        if 'Mimośrody' in self.shaft_sections:
            self._calculate_eccentrics_section()
        if 'Przed mimośrodami' in self.shaft_sections:
            self._calculate_section_before_eccentricities()
        if 'Pomiędzy mimośrodami' in self.shaft_sections:
            self._calculate_section_between_eccentricities()
        if 'Za mimośrodami' in self.shaft_sections:
            self._calculate_section_after_eccentricities()
        
        return self.shaft_sections_plots_attributes
    
    def _calculate_eccentrics_section(self):
        section = 'Mimośrody'
        length = self.shaft_sections[section][0]['l']
        diameter = self.shaft_sections[section][0]['d']

        eccentric1_position = self._shaft_attributes['L1']
        offset = self._shaft_attributes['e']

        # If length of the eccentrics changed, calculate and redraw the new shaft coordinates
        if length != self._shaft_attributes['B']:
            self.is_eccentrics_length_changed = True

            length_between = self._shaft_attributes['x']
            eccentric2_position = eccentric1_position + length + length_between

            self._shaft_attributes['L2'] = eccentric2_position
            self._shaft_attributes['B'] = length
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
    
    def remove_shaft_subsection(self, section_name, subsection_number):
        # Remove the subsection from shaft sections attributes
        if section_name in self.shaft_sections and subsection_number in self.shaft_sections[section_name]:
            del self.shaft_sections[section_name][subsection_number]

            # Adjust the numbering of the remaining subsections
            new_subsections = {}
            for num, data in enumerate(self.shaft_sections[section_name].values()):
                new_subsections[num] = data
            self.shaft_sections[section_name] = new_subsections

            # Recalculate and redraw shaft sections
            return self.calculate_shaft_sections()
