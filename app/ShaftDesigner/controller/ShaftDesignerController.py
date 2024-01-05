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
            section.subsection_data_signal.connect(self._handle_subsection_data)
            section.add_subsection_signal.connect(self._set_limits)
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
        self._sidebar_sections['Mimośród 1'].set_add_subsection_button_visibile(False)
        self._sidebar_sections['Mimośród 2'].set_add_subsection_button_visibile(False)
        self._sidebar_sections['Pomiędzy mimośrodami'].set_add_subsection_button_visibile(False)

        # Disable changing the default values of data entries in certain subsections below
        self._sidebar_sections['Pomiędzy mimośrodami'].subsections[0].set_read_only('l')

        self._shaft_designer.init_sidebar(self._sidebar_sections)

    def set_initial_data(self, data):
        self.shaft_calculator.set_data(data)
        self._chart.init_plots(data)

        # Set limits
        self._set_limits()

        # Redraw shaft section if anything is already drawn on the chart
        if self.shaft_calculator.shaft_sections:
            self._draw_shaft()
    
    def _handle_subsection_data(self, shaft_subsection_attributes):
        # Uptade the shaft drawing
        self._draw_shaft(shaft_subsection_attributes)

        # Enable other sections in the sidebar if both eccentrics sections where plotted, 
        if 'Mimośród 1' and 'Mimośród 2' in self.shaft_calculator.shaft_sections:
            for section in self._sidebar_sections.values():
                section.setEnabled(True)
        
        # Check if add subsection button can be enabled
        section_name = next(iter(shaft_subsection_attributes))
        self.check_if_can_enable_add_subsection_button(section_name)
        
    def _set_limits(self):
        current_subsections = {}

        for section_name, section in self._sidebar_sections.items():
            if section_name not in current_subsections:
                current_subsections[section_name] = []
            for _ in range(section.subsection_count):
                current_subsections[section_name].append(None)

        # Calculate the limits 
        limits = self.shaft_calculator.calculate_shaft_sections_limits(current_subsections)

        if self.shaft_calculator.is_outside_boundaries:
            for subsection in self.shaft_calculator.subsections_to_remove:
                self._sidebar_sections[subsection[0]].remove_subsection(subsection[1])

            self._draw_shaft()

        for section_name, section in self._sidebar_sections.items():
            section.set_limits(limits[section_name])
    
    def _draw_shaft(self, shaft_subsection_attributes = None):
        # Calculate shaft subsections plot attributes and draw them on the chart
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections(shaft_subsection_attributes)
        self._chart.draw_shaft(shaft_plot_attributes)

        # Redraw the shaft coordinates if they were changed
        if self.shaft_calculator.shaft_coordinates_changed is True:
            self._chart._draw_shaft_coordinates()
        
        # Set limits
        self._set_limits()

    def _remove_shaft_subsection(self, section_name, subsection_number):
        # Remove plot attributes in calculators shaft sections
        self.shaft_calculator.remove_shaft_subsection(section_name, subsection_number)

        # Recalculate and redraw shaft sections
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections()
        self._chart.draw_shaft(shaft_plot_attributes)

        # Set limits
        self._set_limits()
        
        # Check if add subsection button can be enabled
        self.check_if_can_enable_add_subsection_button(section_name)

    def check_if_can_enable_add_subsection_button(self, section_name):
        # Enable add button if the last subsection in the sidebar was plotted - do not allow to add multiple subsections at once
        last_subsection_number = self._sidebar_sections[section_name].subsection_count - 1

        if last_subsection_number in self.shaft_calculator.shaft_sections[section_name]:
            self._sidebar_sections[section_name].set_add_subsection_button_enabled(True)   
