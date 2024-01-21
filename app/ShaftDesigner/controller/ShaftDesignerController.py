from ShaftDesigner.model.ShaftCalculator import ShaftCalculator

from ShaftDesigner.view.Chart import Chart
from ShaftDesigner.view.ShaftSection import ShaftSection, EccentricsSection
        
class ShaftDesignerController:
    def __init__(self, view):
        self._shaft_designer = view

        # Set shaft sections names
        self.section_names = ['Wykorbienia', 'Przed Wykorbieniami', 'Pomiędzy Wykorbieniami', 'Za Wykorbieniami']

        # Prepare dict storing sidebar sections
        self._sidebar_sections = {}

        self._init_ui()
        self._connect_signals_and_slots()

        # Set an instance of shaft calculator
        self.shaft_calculator = ShaftCalculator(self.section_names)
    
    def _connect_signals_and_slots(self):
        for section_name, section in self._sidebar_sections.items():
            section.subsection_data_signal.connect(self._handle_subsection_data)
            if section_name != 'Wykorbienia':
                section.remove_subsection_plot_signal.connect(self._remove_shaft_subsection)

    def _init_ui(self):
        # Set an instance of chart
        self._chart = Chart()
        self._shaft_designer.init_chart(self._chart)

        # Set instances of sidebar sections
        for name in self.section_names:
            if name == 'Wykorbienia':
                section = EccentricsSection(name)
            else:
                section = ShaftSection(name)
            self._sidebar_sections[name] = section

        self._shaft_designer.init_sidebar(self._sidebar_sections)

    def set_initial_data(self, functions, shaft_data, shaft_coordinates):
        self.shaft_calculator.set_data(shaft_data)
        self._chart.init_plots(functions, shaft_coordinates)
        # Set number of eccentrics
        self._sidebar_sections['Wykorbienia'].set_subsections_number(shaft_data['n'])

        # Redraw shaft section if anything is already drawn on the chart
        if self.shaft_calculator.shaft_sections:
            self._draw_shaft()
    
    def _handle_subsection_data(self, shaft_subsection_attributes):
        # Update the shaft drawing
        self._draw_shaft(shaft_subsection_attributes)
    
    def _draw_shaft(self, shaft_subsection_attributes = None):
        # Calculate shaft subsections plot attributes and draw them on the chart
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections(shaft_subsection_attributes)
        self._chart.draw_shaft(shaft_plot_attributes)

    def _remove_shaft_subsection(self, section_name, subsection_number):
        # Remove plot attributes in calculators shaft sections
        self.shaft_calculator.remove_shaft_subsection(section_name, subsection_number)

        # Recalculate and redraw shaft sections
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections()
        self._chart.draw_shaft(shaft_plot_attributes)
