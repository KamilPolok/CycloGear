from ShaftDesigner.model.ShaftCalculator import ShaftCalculator

from ShaftDesigner.view.Chart import Chart
from ShaftDesigner.view.ShaftSection import ShaftSection
        
class ShaftDesignerController:
    def __init__(self, view):
        self._shaft_designer = view

        # Set shaft sections names
        self.section_names = ['Mimośród 1', 'Mimośród 2',  'Przed mimośrodami', 'Pomiędzy mimośrodami', 'Za mimośrodami']

        # Prepare dict storing sidebar sections
        self._sidebar_sections = {}

        self._init_ui()
        self._connect_signals_and_slots()

        # Set an instance of shaft calculator
        self.shaft_calculator = ShaftCalculator(self.section_names)
    
    def _connect_signals_and_slots(self):
        for section in self._sidebar_sections.values():
            section.subsection_data_signal.connect(self._draw_shaft)
            section.remove_subsection_plot_signal.connect(self._remove_shaft_subsection)

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
            if section_name != 'Mimośród 1' and section_name != 'Mimośród 2':
                section.setEnabled(False)

        # Disable option to add new subsections for sections below
        self._sidebar_sections['Mimośród 1'].set_add_subsection_button_visibility(False)
        self._sidebar_sections['Mimośród 2'].set_add_subsection_button_visibility(False)
        self._sidebar_sections['Pomiędzy mimośrodami'].set_add_subsection_button_visibility(False)

        # Disable changing the default values of data entries in certain subsections below
        self._sidebar_sections['Pomiędzy mimośrodami'].subsections[0].set_read_only('l')

        self._shaft_designer.init_sidebar(self._sidebar_sections)

    def set_initial_data(self, data):
        self.shaft_calculator.set_data(data)
        self._chart.init_plots(data)

        # Set initial shaft sections attributes
        self._initial_shaft_sections_attributes = { 
            self.section_names[0]: {'l': data['B1'], 'd': data['de']},
            self.section_names[1]: {'l': data['B2'], 'd': data['de']},
            self.section_names[2]: {'l': None, 'd': data['ds']},
            self.section_names[3]: {'l': data['x'], 'd': data['ds']},
            self.section_names[4]: {'l': None, 'd': data['ds']},
        }

        # Set initial shaft sections input values to shaft initial attributes
        for section_name, section in self._sidebar_sections.items():
            for subsection in section.subsections:
                subsection.set_attributes(self._initial_shaft_sections_attributes[section_name])

        # Redraw shaft section if anything is already drawn on the chart
        if self.shaft_calculator.shaft_sections:
            self._draw_shaft()
    
    def _draw_shaft(self, shaft_subsection_attributes = None):
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections(shaft_subsection_attributes)
        self._chart.draw_shaft(shaft_plot_attributes)

        if self.shaft_calculator.shaft_coordinates_changed is True:
            self._chart._draw_shaft_coordinates()

        # If 'Mimośrody' section is calculated, enable other sections in sidebar
        if 'Mimośród 1' and 'Mimośród 2' in self.shaft_calculator.shaft_sections:
            for section in self._sidebar_sections.values():
                section.setEnabled(True)

    def _remove_shaft_subsection(self, section_name, subsection_number):
        shaft_plot_attributes = self.shaft_calculator.remove_shaft_subsection(section_name, subsection_number)
        self._chart.draw_shaft(shaft_plot_attributes)
