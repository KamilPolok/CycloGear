from ShaftDesigner.model.ShaftCalculator import ShaftCalculator
from ShaftDesigner.model.FunctionsCalculator import FunctionsCalculator

from ShaftDesigner.view.Chart.Chart import Chart
from ShaftDesigner.view.Chart.Chart_Plotter import Chart_Plotter
from ShaftDesigner.view.Chart.Chart_ShaftViewer import Chart_ShaftViewer

from ShaftDesigner.view.ShaftSection import ShaftSection, EccentricsSection
        
class ShaftDesignerController:
    def __init__(self, view, mediator):
        self._shaft_designer = view
        self._mediator = mediator

        # Set shaft sections names
        self.section_names = ['Wykorbienia', 'Przed Wykorbieniami', 'Pomiędzy Wykorbieniami', 'Za Wykorbieniami']
        self.is_whole_shaft_designed = False

        # Prepare dict storing sidebar sections
        self._sections = {}
        self._init_ui()
        self._connect_signals_and_slots()

        # Set an instance of shaft calculator
        self.shaft_calculator = ShaftCalculator(self.section_names)

        # Set an instance of functions calculator
        self.functions_calculator = FunctionsCalculator()
    
    def _connect_signals_and_slots(self):
        self._shaft_designer.confirmation_button.clicked.connect(self._emit_shaft_designing_finished)
        for section_name, section in self._sections.items():
            section.subsection_data_signal.connect(self._handle_subsection_data)
            if section_name != 'Wykorbienia':
                section.remove_subsection_plot_signal.connect(self._remove_shaft_subsection)
                section.add_subsection_signal.connect(self._set_limits)

    def _init_ui(self):
        self._init_shaft_sections()
        self._init_chart()
    
    def _init_shaft_sections(self):
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

    def _init_chart(self):
        # Set an instance of chart
        chart = Chart()
        
        self._plotter = Chart_Plotter(chart)
        self._shaft_viewer = Chart_ShaftViewer(chart)

        self._shaft_designer.init_chart(chart)
    
    def _handle_subsection_data(self, shaft_subsection_attributes):
        # Update the shaft drawing
        self._draw_shaft(shaft_subsection_attributes)

        # Enable other sections if eccentrics sections where plotted
        self._enable_sections()

        self._enable_add_subsection_button(shaft_subsection_attributes[0])

        # Enable the confirmation of current shaft design
        self._enable_shaft_design_confirmation()
                
    def _draw_shaft(self, shaft_subsection_attributes = None):
        # Calculate shaft subsections plot attributes and draw them on the chart
        shaft_plot_attributes = self.shaft_calculator.calculate_shaft_sections(shaft_subsection_attributes)
        self._shaft_viewer.draw_shaft(shaft_plot_attributes)

        # Update limits
        self._set_limits()

        # Check if all the limits are met - it can occur when the width of eccentrics
        # or the shaft coordinates get changed
        meets_limits = self.shaft_calculator._check_if_plots_meet_limits()
        if not meets_limits:
            self._draw_shaft()

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
        self._shaft_viewer.draw_shaft(shaft_plot_attributes)
        
        self._enable_add_subsection_button(section_name)
    
    def _enable_sections(self):
        if self.all_sections_enabled == False:
            if len(self.shaft_calculator.shaft_sections_plots_attributes['Wykorbienia']) == self.eccentrics_number:
                for section in self._sections.values():
                    if not section.isEnabled():
                        section.setEnabled(True)
                self.all_sections_enabled == True

    def _enable_shaft_design_confirmation(self):
        if self.is_whole_shaft_designed or self._is_whole_shaft_designed_state_changed():
            self._toogle_remaining_plots_visibility()
            self._shaft_designer.confirmation_button.setEnabled(self.is_whole_shaft_designed)
            
    def _is_whole_shaft_designed_state_changed(self):
        is_whole_shaft_designed_new = self.shaft_calculator.is_whole_shaft_designed()
        if is_whole_shaft_designed_new != self.is_whole_shaft_designed:
            self.is_whole_shaft_designed = is_whole_shaft_designed_new
            return True
        else:
            return False
    
    def _toogle_remaining_plots_visibility(self):
        shaft_steps = self.shaft_calculator.get_shaft_attributes()
        self.functions_calculator.calculate_remaining_functions(shaft_steps)
        self._plotter.set_plots_functions(self.functions_calculator.get_shaft_functions())
    
    def _enable_add_subsection_button(self, section_name):
        # Enable add button if the last subsection in the sidebar was plotted - do not allow to add multiple subsections at once
        if section_name != 'Wykorbienia':
            last_subsection_number = self._sections[section_name].subsection_count - 1
            if self._sections[section_name].subsection_count == 0 or (section_name in self.shaft_calculator.shaft_sections_plots_attributes and
            last_subsection_number in self.shaft_calculator.shaft_sections_plots_attributes[section_name]):
                self._sections[section_name].set_add_subsection_button_enabled(True)

    def _emit_shaft_designing_finished(self):
        self.shaft_calculator.save_data(self._data)
        self._mediator.emit_shaft_designing_finished()

    def update_shaft_data(self, data):
        # Update shaft initial data
        self._data = data

        # (Re)calculate initial functions and attributes
        self.functions_calculator.calculate_initial_functions_and_attributes(data)

        # (Re)set shaft initial coordinates
        self._shaft_viewer.init_shaft(self.functions_calculator.get_shaft_coordinates())

        # (Re)set number of eccentrics
        self.eccentrics_number = data['n'][0]
        self._sections['Wykorbienia'].set_subsections_number(self.eccentrics_number)

        # (Re)set shaft initial attributes 
        self.shaft_calculator.set_data(self.functions_calculator.get_shaft_initial_attributes())

        # Update limits
        self._set_limits()
        # Redraw shaft and recalculate remaining functions
        if self.shaft_calculator.shaft_sections:
            self._draw_shaft()
            self._enable_shaft_design_confirmation()

        # (Re)draw shaft plots
        self._plotter.set_plots_functions(self.functions_calculator.get_shaft_functions(), self.functions_calculator.get_shaft_z())
    
    def get_shaft_data(self):
        return self.shaft_calculator.shaft_sections
    
    def set_shaft_data(self, data):
        for section_name, section in data.items():
            for subsection_number, subsection in section.items():
                if section_name != 'Wykorbienia':
                    self._sections[section_name].add_subsection()
                data = (section_name, subsection_number, subsection, None)
                self._draw_shaft(data)
                self._enable_sections()

        self._enable_shaft_design_confirmation()
