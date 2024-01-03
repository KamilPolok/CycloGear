class ShaftCalculator:
    def __init__(self, section_names):
        self._section_names = section_names
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
    
    def _prepare_for_calculations(self, shaft_subsection_attributes):
        # Init the flags
        self.shaft_coordinates_changed = False

        # Set the same diameter of eccentrics
        if shaft_subsection_attributes:
            if 'Mimośród 1' in shaft_subsection_attributes:
                if 'Mimośród 2' in self.shaft_sections:
                    self.shaft_sections['Mimośród 2'][0]['d'] = self.shaft_sections['Mimośród 1'][0]['d']
            elif 'Mimośród 2' in shaft_subsection_attributes:
                if 'Mimośród 1' in self.shaft_sections:
                    self.shaft_sections['Mimośród 1'][0]['d'] = self.shaft_sections['Mimośród 2'][0]['d'] 

    def calculate_shaft_sections(self, shaft_subsection_attributes = None):
        # Save subsection attrbutes
        self._save_shaft_sections_attributes(shaft_subsection_attributes)

        # Prepare data before performing calculations
        self._prepare_for_calculations(shaft_subsection_attributes)

        # Prepare dict storing shaft subsections plots attributes
        self.shaft_sections_plots_attributes = {section_name: {} for section_name in self._section_names}

        # Calculate shaft sections plots attributes
        if 'Mimośród 1' in self.shaft_sections:
            self._calculate_eccentric1_section()
        if 'Mimośród 2' in self.shaft_sections:
            self._calculate_eccentric2_section()
        if 'Przed mimośrodami' in self.shaft_sections:
            self._calculate_section_before_eccentricities()
        if 'Pomiędzy mimośrodami' in self.shaft_sections:
            self._calculate_section_between_eccentricities()
        if 'Za mimośrodami' in self.shaft_sections:
            self._calculate_section_after_eccentricities()
        
        return self.shaft_sections_plots_attributes
    
    def _calculate_eccentric1_section(self):
        section = 'Mimośród 1'
        length = self.shaft_sections[section][0]['l']
        diameter = self.shaft_sections[section][0]['d']

        position = self._shaft_attributes['L1']
        offset = self._shaft_attributes['e']

        # If second eccentric section does not exists yet, take care of adjusting the shaft coordinates
        if 'Mimośród 2' not in self.shaft_sections:
            length_between = self._shaft_attributes['x']
            eccentric2_position = position + 0.5 * length + 0.5 * self._shaft_attributes['B1'] + length_between
            self._shaft_attributes['L2'] = eccentric2_position
            self.shaft_coordinates_changed = True

        start_z = position - length / 2
        start_y = offset - diameter / 2

        self.shaft_sections_plots_attributes[section][0] = [(start_z, start_y), length, diameter]

    def _calculate_eccentric2_section(self):
        section = 'Mimośród 2'
        length = self.shaft_sections[section][0]['l']
        diameter = self.shaft_sections[section][0]['d']

        position = self._shaft_attributes['L2']
        offset = self._shaft_attributes['e']
        length_between = self._shaft_attributes['x']

        if 'Mimośród 1' in self.shaft_sections:
            eccentric2_position = self._shaft_attributes['L1'] + 0.5 * length + 0.5 * self.shaft_sections['Mimośród 1'][0]['l'] + length_between

            # If length of the second eccentric changed, calculate and redraw the new shaft coordinates
            if position != eccentric2_position:
                self.shaft_coordinates_changed = True

                position = eccentric2_position
                self._shaft_attributes['L2'] = eccentric2_position

        start_z = position - length / 2
        start_y = -offset - diameter / 2

        self.shaft_sections_plots_attributes[section][0] = [(start_z, start_y), length, diameter]

    def _calculate_section_between_eccentricities(self):
        # Draw the shaft section between the eccentrics
        section ='Pomiędzy mimośrodami'
        length = self.shaft_sections[section][0]['l']
        diameter = self.shaft_sections[section][0]['d']
        start_z = self._shaft_attributes['L1'] + self.shaft_sections['Mimośród 1'][0]['l'] / 2
        start_y = -diameter / 2

        self.shaft_sections_plots_attributes[section][0] = [(start_z, start_y), length, diameter]

    def _calculate_section_before_eccentricities(self):
        # Draw the shaft section before the first eccentric
        section ='Przed mimośrodami'

        start_z = self._shaft_attributes['L1'] - self.shaft_sections['Mimośród 1'][0]['l'] / 2

        for subsection_number, subsection_data in self.shaft_sections[section].items():
            length = subsection_data['l']
            diameter = subsection_data['d']
            start_z -= length
            start_y = -diameter / 2

            self.shaft_sections_plots_attributes[section][subsection_number] = [(start_z, start_y), length, diameter]
        
    def _calculate_section_after_eccentricities(self):
        # Draw the shaft section after the second eccentric
        section ='Za mimośrodami'
        start_z = self._shaft_attributes['L2'] + self.shaft_sections['Mimośród 2'][0]['l'] / 2

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
