from ShaftDesigner.view.ShaftDesigner import ShaftDesigner

from ShaftDesigner.model.ShaftCalculator import ShaftCalculator
from ShaftDesigner.model.FunctionsCalculator import FunctionsCalculator

from ShaftDesigner.view.ShaftSection import ShaftSection, EccentricsSection

from Utility.MessageHandler import MessageHandler
        
class ShaftDesignerController:
    def __init__(self, view: ShaftDesigner, mediator):
        self._shaft_designer = view
        self._mediator = mediator

        # Set shaft sections names
        self.section_names = ['Wykorbienia', 'Przed Wykorbieniami', 'Za Wykorbieniami']
        self.is_whole_shaft_designed = False

        # Prepare dict storing sidebar sections
        self._sections = {}
        self._init_ui()
        self._connect_signals_and_slots()

        # Set an instance of shaft calculator
        self.shaft_calculator = ShaftCalculator()

        # Set an instance of functions calculator
        self.functions_calculator = FunctionsCalculator()
    
    def _connect_signals_and_slots(self):
        self._shaft_designer.confirmation_button.clicked.connect(self._on_finish_draft)
        for section_name, section in self._sections.items():
            section.subsection_data_signal.connect(self._handle_subsection_data)
            if section_name != 'Wykorbienia':
                section.remove_subsection_plot_signal.connect(self._remove_shaft_subsection)
                section.add_subsection_signal.connect(self._set_limits)

    def _init_ui(self):
        self._init_shaft_sections()
    
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

        self._shaft_designer.set_sidebar_sections(self._sections)
    
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
        self._shaft_designer.shaft_viewer.draw_shaft(shaft_plot_attributes)

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
        self._shaft_designer.shaft_viewer.draw_shaft(shaft_plot_attributes)
        
        self._enable_add_subsection_button(section_name)
        self._enable_shaft_design_confirmation()
    
    def _enable_sections(self):
        if self.all_sections_enabled == False:
            if 'Wykorbienia' in self.shaft_calculator.shaft_sections and len(self.shaft_calculator.shaft_sections['Wykorbienia']) == self.eccentrics_number:
                for section in self._sections.values():
                    if not section.isEnabled():
                        section.setEnabled(True)
                self.all_sections_enabled == True

    def _enable_shaft_design_confirmation(self):
        is_whole_shaft_designed_state_changed = self._is_whole_shaft_designed_state_changed()
        
        if self.is_whole_shaft_designed or is_whole_shaft_designed_state_changed:
            self._toogle_remaining_plots_visibility()
            self._shaft_designer.confirmation_button.setEnabled(self.is_whole_shaft_designed)
            if not self.is_whole_shaft_designed:
                self._shaft_designer.set_draft_finished_title(False)
            
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
        self._set_functions_plots(self.functions_calculator.get_shaft_functions())
    
    def _enable_add_subsection_button(self, section_name):
        # Enable add button if the last subsection in the sidebar was plotted - do not allow to add multiple subsections at once
        if section_name != 'Wykorbienia':
            last_subsection_number = self._sections[section_name].subsection_count - 1
            if self._sections[section_name].subsection_count == 0 or (section_name in self.shaft_calculator.shaft_sections and
            last_subsection_number in self.shaft_calculator.shaft_sections[section_name]):
                self._sections[section_name].set_add_subsection_button_enabled(True)

    def _set_functions_plots(self, shaft_functions):
        def update_plot_menus(id, function_details, key, plot_menu):
            if id not in plot_menu.getItems():
                label, description = function_details[:2]
                plot_menu.addItem(id, label, description)
            if function_details[3] is None:
                del shaft_functions[key][id]
                plot_menu.enableItem(id, False)
            else:
                plot_menu.enableItem(id, True)

        plots = {}
        for plot_key in ['f(z)', 'dmin(z)']:
            if plot_key in shaft_functions:
                for plot_id, function_details in list(shaft_functions[plot_key].items()):
                    plot_menu = self._shaft_designer._plots_menu if plot_key == 'f(z)' else self._shaft_designer._min_diameters_menu
                    update_plot_menus(plot_id, function_details, plot_key, plot_menu)
                    plots.update(shaft_functions[plot_key])
    
        self._shaft_designer.plotter.set_functions_plots(shaft_functions['z'], plots)

    def _on_finish_draft(self):
        self.shaft_calculator.save_data(self._data)
        self._shaft_designer.set_draft_finished_title(True)
        MessageHandler.information(self._shaft_designer,'', 'Projekt został zatwierdzony')
        self._mediator.emit_shaft_designing_finished()

    def update_shaft_data(self, data):
        # Update shaft initial data
        self._data = data

        # (Re)calculate initial functions and attributes
        self.functions_calculator.calculate_initial_functions_and_attributes(data)

        # (Re)set shaft initial coordinates
        self._shaft_designer.shaft_viewer.init_shaft(self.functions_calculator.get_shaft_coordinates())

        # (Re)set number of eccentrics
        self.eccentrics_number = data['n'][0]
        if self.eccentrics_number < 2 and 'Pomiędzy Wykorbieniami' in self._sections:
            self._shaft_designer.remove_section_from_sidebar(self._sections['Pomiędzy Wykorbieniami'])
            del self._sections['Pomiędzy Wykorbieniami']
            if 'Pomiędzy Wykorbieniami' in self.shaft_calculator.shaft_sections:
                del self.shaft_calculator.shaft_sections['Pomiędzy Wykorbieniami']
        elif self.eccentrics_number >= 2 and 'Pomiędzy Wykorbieniami' not in self._sections:
            section = ShaftSection('Pomiędzy Wykorbieniami')
            section.setEnabled(False)
            self._enable_sections()
            self._sections['Pomiędzy Wykorbieniami'] = section
            self._shaft_designer.append_section_to_sidebar(section)
            section.subsection_data_signal.connect(self._handle_subsection_data)
            section.remove_subsection_plot_signal.connect(self._remove_shaft_subsection)
            section.add_subsection_signal.connect(self._set_limits)
        self._sections['Wykorbienia'].set_subsections_number(self.eccentrics_number)

        # (Re)set shaft initial attributes 
        self.shaft_calculator.set_data(self.functions_calculator.get_shaft_initial_attributes())

        # Update limits
        self._set_limits()
        # Redraw shaft and recalculate remaining functions
        if self.shaft_calculator.shaft_sections:
            self._draw_shaft()
            self._enable_shaft_design_confirmation()
            self.update_bearing_data()

        # (Re)draw shaft plots
        self._set_functions_plots(self.functions_calculator.get_shaft_functions())

    def update_bearing_data(self, bearing_attributes=None):
        """
        Calculate bearings dimensions and update them in shaft viewer.

        Args:
            bearing_attributes (dict): single bearing attributes.
        """
        bearings_plot_attributes = self.shaft_calculator.calculate_bearings(bearing_attributes)
        self._shaft_designer.shaft_viewer.set_bearings(bearings_plot_attributes)

    def get_shaft_data(self):
        return self.shaft_calculator.shaft_sections

    def set_shaft_data(self, data):
        for section_name, section in data.items():
            for subsection_number, subsection in section.items():
                if section_name != 'Wykorbienia':
                    self._sections[section_name].add_subsection()
                data = (section_name, int(subsection_number), subsection, None)
                self._draw_shaft(data)
                self._enable_sections()

        self._enable_shaft_design_confirmation()
