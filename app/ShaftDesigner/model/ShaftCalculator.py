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
        self.updated_eccentrics_diameter = None

        if shaft_subsection_attributes:
            if 'Mimośród 1' in shaft_subsection_attributes:
                if 'Mimośród 2' in self.shaft_sections:
                    self.updated_eccentrics_diameter = self.shaft_sections['Mimośród 1'][0]['d']
                    self.shaft_sections['Mimośród 2'][0]['d'] = self.updated_eccentrics_diameter
            elif 'Mimośród 2' in shaft_subsection_attributes:
                if 'Mimośród 1' in self.shaft_sections:
                    self.updated_eccentrics_diameter = self.shaft_sections['Mimośród 2'][0]['d']
                    self.shaft_sections['Mimośród 1'][0]['d'] = self.updated_eccentrics_diameter
    
    def calculate_shaft_sections_limits(self, current_subsections):
        self.limits = {
            'Mimośród 1': {0: {'l': {'min': 0, 'max': 2 * (self._shaft_attributes['L1'] - self._shaft_attributes['LA'])}, 
                           'd': {'min': self._shaft_attributes['de'], 'max': 1000}}},
            'Mimośród 2': {0: {'l': {'min': 0, 'max': (self._shaft_attributes['LB'] - self._shaft_attributes['L1']) - 0.5 * self._shaft_attributes['B1'] - self._shaft_attributes['x']}, 
                           'd': {'min': self._shaft_attributes['de'], 'max': 1000}}},
            'Przed mimośrodami': {0: {'l': {'min': 0, 'max': None}, 
                                  'd': {'min': self._shaft_attributes['ds'], 'max': 1000}}},
            'Pomiędzy mimośrodami': {0: {'l': {'min': 0, 'max': self._shaft_attributes['x']}, 
                                     'd': {'min': self._shaft_attributes['ds'], 'max': 1000}}},
            'Za mimośrodami': {0: {'l': {'min': 0, 'max': None}, 
                               'd': {'min': self._shaft_attributes['ds'], 'max': 1000}}},
        }

        for section_name, section in current_subsections.items():
            if 'Mimośród 1' in self.shaft_sections and 'Mimośród 2' in self.shaft_sections:
                self.limits['Przed mimośrodami'][0]['l']['max'] = max(self._shaft_attributes['L1'] - 0.5 * self.shaft_sections['Mimośród 1'][0]['l'], 0)
                self.limits['Za mimośrodami'][0]['l']['max'] = max(self._shaft_attributes['L'] - self._shaft_attributes['L2'] - 0.5 * self.shaft_sections['Mimośród 2'][0]['l'], 0)
                if len(section) > 1:
                    for subsection_number in range(1, len(section)):
                        previous_subsection_number = subsection_number - 1
                        l_min = self.limits[section_name][previous_subsection_number]['l']['min']
                        l_max = max(self.limits[section_name][previous_subsection_number]['l']['max'] - self.shaft_sections[section_name][previous_subsection_number]['l'], 0)
                        d_min = self.limits[section_name][previous_subsection_number]['d']['min']
                        d_max = self.limits[section_name][previous_subsection_number]['d']['max']

                        self.limits[section_name][subsection_number] = {'l': {'min': l_min, 'max': l_max}, 'd': {'min': d_min, 'max': d_max}}
        
        self._check_if_plots_are_within_boundaries()

        return self.limits

    def _check_if_plots_are_within_boundaries(self):
        self.subsections_to_remove = []
        self.is_outside_boundaries = False
        for section_name, section in self.shaft_sections.items():
            remove_remaining = False
            for subsection_number, subsection in section.items():
                if not remove_remaining:
                    for attribute, value in subsection.items():
                        if value < self.limits[section_name][subsection_number][attribute]['min']:
                            subsection[attribute] = self.limits[section_name][subsection_number][attribute]['min']
                            if subsection[attribute] == 0:
                                self.subsections_to_remove.append((section_name, subsection_number))
                            self.is_outside_boundaries = True
                            remove_remaining = True
                        elif value > self.limits[section_name][subsection_number][attribute]['max']:
                            subsection[attribute] = self.limits[section_name][subsection_number][attribute]['max']
                            self.is_outside_boundaries = True
                            remove_remaining = True
                else:
                    self.subsections_to_remove.append((section_name, subsection_number))

        for subsection in self.subsections_to_remove:
                self.remove_shaft_subsection(subsection[0], subsection[1])
                del self.limits[subsection[0]][subsection[1]]

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
        self._shaft_attributes['B1'] = length
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
