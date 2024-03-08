class ShaftCalculator:
    def __init__(self, section_names):
        self._section_names = section_names
        self.shaft_sections = {}
        self.limits = {}

    def _save_shaft_sections_attributes(self, attributes):
        if attributes:
            section_name = attributes[0]
            section_number = attributes[1]
            data = attributes[2]
            common_section_data = attributes[3]
            
            if section_name not in self.shaft_sections:
                self.shaft_sections[section_name] = {}
            
            self.shaft_sections[section_name][section_number] = data

            if isinstance(common_section_data, dict):
                for subsection_attributes in self.shaft_sections[section_name].values():
                    subsection_attributes.update(common_section_data)

    def calculate_shaft_sections(self, shaft_subsection_attributes = None):
        # Save subsection attrbutes
        self._save_shaft_sections_attributes(shaft_subsection_attributes)

        # Prepare dict storing shaft subsections plots attributes
        self._shaft_sections_plots_attributes = {section_name: {} for section_name in self._section_names}

        # Calculate shaft sections plots attributes
        if 'Wykorbienia' in self.shaft_sections:
            self._calculate_eccentricities_section()
        if 'Przed Wykorbieniami' in self.shaft_sections:
            self._calculate_section_before_eccentricities()
        if 'Pomiędzy Wykorbieniami' in self.shaft_sections:
            self._calculate_section_between_eccentricities()
        if 'Za Wykorbieniami' in self.shaft_sections:
            self._calculate_section_after_eccentricities()
        
        return self._shaft_sections_plots_attributes
    
    def _calculate_eccentricities_section(self):
        section = 'Wykorbienia'
        for subsection_number, subsection_data in self.shaft_sections[section].items():
            length = subsection_data['l']
            diameter = subsection_data['d']
            position = self._shaft_attributes[f'L{subsection_number+1}']
            self._shaft_attributes[F'B{subsection_number+1}'] = length
            offset = self._shaft_attributes['e'] * (-1)**subsection_number

            start_z = position - length / 2
            start_y = - diameter / 2 + offset 

            self._shaft_sections_plots_attributes[section][subsection_number] = {'start': (start_z, start_y), 'l': length, 'd': diameter, 'e': offset}

    def _calculate_section_between_eccentricities(self):
        # Draw the shaft section between the eccentrics
        section = 'Pomiędzy Wykorbieniami'
        start_z = self._shaft_attributes['L1'] + self.shaft_sections['Wykorbienia'][0]['l'] / 2

        for subsection_number, subsection_data in self.shaft_sections[section].items():
            length = subsection_data['l']
            diameter = subsection_data['d']
            start_y = -diameter / 2

            self._shaft_sections_plots_attributes[section][subsection_number] = {'start': (start_z, start_y), 'l': length, 'd': diameter}

            start_z += length # Update start_z for the next subsection

    def _calculate_section_before_eccentricities(self):
        # Draw the shaft section before the first eccentric
        section = 'Przed Wykorbieniami'

        start_z = self._shaft_attributes['L1'] - self.shaft_sections['Wykorbienia'][0]['l'] / 2

        for subsection_number, subsection_data in self.shaft_sections[section].items():
            length = subsection_data['l']
            diameter = subsection_data['d']
            start_z -= length
            start_y = -diameter / 2

            self._shaft_sections_plots_attributes[section][subsection_number] = {'start': (start_z, start_y), 'l': length, 'd': diameter}
        
    def _calculate_section_after_eccentricities(self):
        # Draw the shaft section after the second eccentric
        section = 'Za Wykorbieniami'
        start_z = self._shaft_attributes['L2'] + self.shaft_sections['Wykorbienia'][1]['l'] / 2

        for subsection_number, subsection_data in self.shaft_sections[section].items():
            length = subsection_data['l']
            diameter = subsection_data['d']
            start_y = -diameter / 2
            
            self._shaft_sections_plots_attributes[section][subsection_number] = {'start': (start_z, start_y), 'l': length, 'd': diameter}
            
            start_z += length  # Update start_z for the next subsection
    
    def _check_if_plots_meet_limits(self):
        meets_limits = True

        for section_name, section in self.shaft_sections.items():
            for subsection_number, subsection in section.items():
                for attribute, value in subsection.items():
                    min = self.limits[section_name][subsection_number][attribute]['min']
                    max = self.limits[section_name][subsection_number][attribute]['max']
                    if min <= value <= max:
                        continue
                    else:
                        meets_limits = False
                        if value < min:
                                subsection[attribute] = min
                        elif value > max:
                                subsection[attribute] = max

        return meets_limits

    def remove_shaft_subsection(self, section_name, subsection_number):
        # Remove the subsection from shaft sections attributes
        if section_name in self.shaft_sections and subsection_number in self.shaft_sections[section_name]:
            del self.shaft_sections[section_name][subsection_number]

            # Adjust the numbering of the remaining subsections
            new_subsections = {}
            if len(self.shaft_sections[section_name]):
                for num, data in enumerate(self.shaft_sections[section_name].values()):
                    new_subsections[num] = data
                self.shaft_sections[section_name] = new_subsections
            else:
                del self.shaft_sections[section_name]
                
    def calculate_limits(self, current_subsections):
        ds = self._shaft_attributes['ds']
        de = self._shaft_attributes['de']
        B = self._shaft_attributes['B']
        x = self._shaft_attributes['x']
        LA = self._shaft_attributes['LA']
        LB = self._shaft_attributes['LB']
        L1 = self._shaft_attributes['L1']
        L2 = self._shaft_attributes['L2']
        L = self._shaft_attributes['L']
        B1 = self._shaft_attributes['B1']
        B2 = self._shaft_attributes['B2']
        
        # Set initial limits for eccentrics
        self.limits = {
            'Wykorbienia' : {0: {'d': {'min': de, 'max': 1000},
                                  'l': {'min': B, 'max': 2 * min(L1 - LA, x - 0.5 * B2 + B)}},
                             1: {'d': {'min': de, 'max': 1000},
                                 'l': {'min': B, 'max': 2 * min(LB - L2, x - 0.5 * B1 + B)}}
            }
        }

        for section_name, section in current_subsections.items():
            for subsection_number, section in enumerate(section):
                lmin = 0
                dmin = ds
                dmax = 1000
                if subsection_number == 0:
                    self.limits[section_name] = {}
                    if section_name == 'Przed Wykorbieniami':
                        lmax = max(L1 - 0.5 * B1, 0)
                    if section_name == 'Pomiędzy Wykorbieniami':
                        lmax = L2 - L1 - 0.5 * (B1 + B2)
                    if section_name == 'Za Wykorbieniami':
                        lmax = max(L - L2 - 0.5 * B2, 0)
                else:
                    previous_subsection = self.limits[section_name][subsection_number - 1]
                    lmax = max(previous_subsection['l']['max'] - self.shaft_sections[section_name][subsection_number - 1]['l'], 0)
                self.limits[section_name][subsection_number] = {'d': {'min': dmin, 'max': dmax}, 'l': {'min': lmin, 'max': lmax}}

        return self.limits
    
    def is_whole_shaft_designed(self):
        total_length = 0
    
        for section in self._shaft_sections_plots_attributes.values():
            for subsection_attributes in section.values(): 
                length = subsection_attributes['l']
                total_length += length
        
        return total_length == self._shaft_attributes['L']

    def get_shaft_attributes(self):
        shaft_steps = []
        for section in self._shaft_sections_plots_attributes.values():
            for subsection_attributes in section.values():
                z = subsection_attributes['start'][0]
                l = subsection_attributes['l']
                d = subsection_attributes['d']

                shaft_steps.append({'z': z, 'l': l, 'd': d})
        
        shaft_steps.sort(key=lambda x: x['z'])
        
        return shaft_steps

    def set_data(self, shaft_attributes):
        self._shaft_attributes = shaft_attributes

    def save_data(self, data):
        LA = self._shaft_attributes['LA']
        LB = self._shaft_attributes['LB']
        L1 = self._shaft_attributes['L1']
       
        support_places = [ [LA, None], [LB, None], [L1, None],]

        shaft_steps = self.get_shaft_attributes()
        for support in support_places:
            for step in shaft_steps:
                if step['z'] + step['l'] > support[0]:
                    support[1] = step['d']
                    break
        
        data['Bearings']['support_A']['dip'][0] = support_places[0][1]
        data['Bearings']['support_B']['dip'][0] = support_places[1][1]
        data['Bearings']['eccentrics']['dip'][0] = support_places[2][1]
