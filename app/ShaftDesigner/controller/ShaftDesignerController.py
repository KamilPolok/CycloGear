from ShaftDesigner.model.ShaftCalculator import ShaftCalculator

from ShaftDesigner.view.Chart import Chart
from ShaftDesigner.view.ShaftSection import ShaftSection, EccentricsSection
        
class ShaftDesignerController:
    def __init__(self, view):
        self._shaft_designer = view

        # Set shaft sections names
        self.section_names = ['Wykorbienia', 'Przed Wykorbieniami', 'Pomiędzy Wykorbieniami', 'Za Wykorbieniami']

        # Prepare dict storing sidebar sections
        self._sections = {}

        self._init_ui()
        self._connect_signals_and_slots()

        # Set an instance of shaft calculator
        self.shaft_calculator = ShaftCalculator(self.section_names)
    
    def _connect_signals_and_slots(self):
        for section_name, section in self._sections.items():
            section.subsection_data_signal.connect(self._handle_subsection_data)
            if section_name != 'Wykorbienia':
                section.remove_subsection_plot_signal.connect(self._remove_shaft_subsection)
                section.add_subsection_signal.connect(self._set_limits)

    def _init_ui(self):
        # Set instances of sidebar sections
        for name in self.section_names:
            if name == 'Wykorbienia':
                section = EccentricsSection(name)
            else:
                section = ShaftSection(name)
                section.setDisabled(True)
            self._sections[name] = section

        self.all_sections_enabled = False

        self._shaft_designer.init_sidebar(self._sections)
    
        # Set an instance of chart
        self._chart = Chart()
        self._shaft_designer.init_chart(self._chart)

    def set_initial_data(self, functions, shaft_data, shaft_coordinates):
        self.shaft_calculator.set_data(shaft_data)
        self._chart.init_plots(functions, shaft_coordinates)
        # Set number of eccentrics
        self.eccentrics_number = shaft_data['n']
        self._sections['Wykorbienia'].set_subsections_number(self.eccentrics_number)

        # Set limits
        self._set_limits()

        # Redraw shaft section if anything is already drawn on the chart
        if self.shaft_calculator.shaft_sections:
            self._draw_shaft()
    
    def _handle_subsection_data(self, shaft_subsection_attributes):
        # Update the shaft drawing
        self._draw_shaft(shaft_subsection_attributes)

        # Update limits
        self._set_limits()

        # Check if all the limits are met - it can occur when the width of eccentrics
        # or the shaft coordinates get changed
        meets_limits = self.shaft_calculator._check_if_plots_meet_limits()
        if not meets_limits:
            self._draw_shaft()

        # Enable other sections if eccentrics sections where plotted
        if self.all_sections_enabled == False:
            self._enable_sections()

        self._enable_add_subsection_button(shaft_subsection_attributes[0])
                
    def _draw_shaft(self, shaft_subsection_attributes = None):
        # Calculate shaft subsections plot attributes and draw them on the chart
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections(shaft_subsection_attributes)
        self._chart.draw_shaft(shaft_plot_attributes)

    def _set_limits(self):
        current_subsections = {}
        for section_name, section in self._sections.items():
            if section_name != 'Wykorbienia':
                current_subsections[section_name] = [None] * section.subsection_count
        limits = self.shaft_calculator.calculate_limits(current_subsections)

        for section_name, section in limits.items():
            self._sections[section_name].set_limits(section)

    def _remove_shaft_subsection(self, section_name, subsection_number):
        # Remove plot attributes in calculators shaft sections
        self.shaft_calculator.remove_shaft_subsection(section_name, subsection_number)

        # Recalculate and redraw shaft sections
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections()
        self._chart.draw_shaft(shaft_plot_attributes)

        self._enable_add_subsection_button(section_name)

    def _enable_sections(self):
        if len(self.shaft_calculator.shaft_sections_plots_attributes['Wykorbienia']) == self.eccentrics_number:
            for section in self._sections.values():
                if not section.isEnabled():
                    section.setEnabled(True)
            self.all_sections_enabled == True

    def _enable_add_subsection_button(self, section_name):
        # Enable add button if the last subsection in the sidebar was plotted - do not allow to add multiple subsections at once
        if section_name != 'Wykorbienia':
            last_subsection_number = self._sections[section_name].subsection_count - 1
            if self._sections[section_name].subsection_count == 0 or (section_name in self.shaft_calculator.shaft_sections_plots_attributes and
            last_subsection_number in self.shaft_calculator.shaft_sections_plots_attributes[section_name]):
                self._sections[section_name].set_add_subsection_button_enabled(True)