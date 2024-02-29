from InputShaft.Mediator import Mediator
from InputShaft.view.InputShaft import InputShaft
from InputShaft.model.InputShaftCalculator import InputShaftCalculator

from InputShaft.Tabs.PreliminaryDataTab import PreliminaryDataTab
from InputShaft.Tabs.PreliminaryDataTabController import PreliminaryDataTabController
from InputShaft.Tabs.PreliminaryDataTabCalculator import PreliminaryDataTabCalculator

from InputShaft.Tabs.BearingsTab import BearingsTab
from InputShaft.Tabs.BearingsTabController import BearingsTabController

from InputShaft.Tabs.PowerLossTab import PowerLossTab
from InputShaft.Tabs.PowerLossTabController import PowerLossTabController

from InputShaft.Tabs.ResultsTab import ResultsTab
from InputShaft.Tabs.ResultsTabController import ResultsTabController

from ShaftDesigner.controller.ShaftDesignerController import ShaftDesignerController
from ShaftDesigner.view.ShaftDesigner import ShaftDesigner

class InputShaftController:
    """
    Controller for the InputShaft in the application.

    This class handles the interactions between the model (data) and the view (InputShaft),
    including initializing the view with data, connecting signals and slots, and handling
    user interactions.
    """
    def __init__(self, model: InputShaftCalculator, view: InputShaft):
        """
        Initialize the InputShaftController.W

        :param data: The data for the application.
        :param view: The InputShaft (QWidget) instance of the input shaft coomponent's GUI.
        """
        self._input_shaft = view
        self._calculator = model

        self._startup()
        self._connect_signals_and_slots()

    def _startup(self):
        """Initialize the input shaft widget with necessary data, set up tabs and initialize the shaft designer"""
        self._mediator = Mediator()
        self._init_tabs()
        self._init_shaft_designer()

    def _init_tabs(self):
        tab_id = 1

        tab1 = PreliminaryDataTab(self._input_shaft)
        tab1_calculator = PreliminaryDataTabCalculator()
        tab1_controller = PreliminaryDataTabController(tab_id, tab1, tab1_calculator, self._mediator)

        tab_id +=1
        tab2 = BearingsTab(self._input_shaft)
        tab2_controller = BearingsTabController(tab_id, tab2, self._mediator)

        tab_id +=1
        tab3 = PowerLossTab(self._input_shaft)
        tab3_controller = PowerLossTabController(tab_id, tab3, self._mediator)

        tab_id +=1
        tab4 = ResultsTab(self._input_shaft)
        tab4_controller = ResultsTabController(tab_id, tab4, self._mediator)

        self.tabs = [tab1, tab2, tab3, tab4]
        self.tab_controllers = [tab1_controller, tab2_controller, tab3_controller, tab4_controller]
        tab_titles = ['Założenia wstępne', 'Dobór łożysk', 'Straty Mocy', 'Wyniki obliczeń']

        for tab in self.tab_controllers:
            data = self._calculator.get_data()
            tab.init_state(data)

        self._input_shaft.init_tabs(self.tabs, tab_titles)

    def _init_shaft_designer(self):
        # Set an instance of shaft designer
        window_title = f'CycloGear2023 - Projektant Wału Wejściowego'
        self._shaft_designer = ShaftDesigner(window_title)

        # Set an instance of shaft designer controller
        self._shaft_designer_controller = ShaftDesignerController(self._shaft_designer, self._mediator)

    def _connect_signals_and_slots(self):
        """
        Connect signals and slots for interactivity in the application.

        This method sets up connections between UI elements and their corresponding
        actions or handlers.
        """
        self._input_shaft.preview_button.clicked.connect(self._open_shaft_designer_window)
        self._mediator.shaftDesigningFinished.connect(self._on_shaft_designing_finished)

        self._mediator.selectMaterial.connect(self._on_select_materials)

        self._mediator.selectSupportABearing.connect(self._on_select_support_A_bearing)
        self._mediator.selectSupportBBearing.connect(self._on_select_support_B_bearing)
        self._mediator.selectCentralBearing.connect(self._on_select_central_bearing)

        self._mediator.selectSupportABearingRollingElement.connect(self._on_select_support_A_bearing_rolling_element)
        self._mediator.selectSupportBBearingRollingElement.connect(self._on_select_support_B_bearing_rolling_element)
        self._mediator.selectCentralBearingRollingElement.connect(self._on_select_central_bearing_rolling_element)

        self._mediator.updateComponentData.connect(self._update_component_data)

    def _update_component_data(self, tab_id, data):
        self._calculator.update_data(data)

        if tab_id == 1:
            self._update_input_shaft_attributes()
        elif tab_id == 2:
            self._on_update_bearings_data()
        elif tab_id == 3:
            self._on_update_power_loss_data()

    def _open_shaft_designer_window(self):
        if self._shaft_designer.isHidden():
            self._shaft_designer.show()

    def _on_select_materials(self):
        self._calculator.open_shaft_material_selection(self.tabs[0].update_selected_material)

    def _on_select_support_A_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_support_A_bearing_load_capacity()
        self._calculator.open_support_A_bearing_selection(self.tabs[1].update_selected_support_A_bearing)

    def _on_select_support_B_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_support_B_bearing_load_capacity()
        self._calculator.open_support_B_bearing_selection(self.tabs[1].update_selected_support_B_bearing)

    def _on_select_central_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_central_bearing_load_capacity()
        self._calculator.open_central_bearing_selection(self.tabs[1].update_selected_central_bearing)

    def _on_update_bearings_data(self):
        self._calculator.calculate_bearings_attributes()

    def _on_select_support_A_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_support_A_bearing_rolling_element_selection(self.tabs[2].update_selected_support_A_bearing_rolling_element)
            
    def _on_select_support_B_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_support_B_bearing_rolling_element_selection(self.tabs[2].update_selected_support_B_bearing_rolling_element)
            
    def _on_select_central_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_central_bearing_rolling_element_selection(self.tabs[2].update_selected_central_bearing_rolling_element)

    def _on_update_power_loss_data(self):
        self._calculator.calculate_bearings_power_loss()
         
    def _update_input_shaft_attributes(self):
        """
        Calculate attributes for the input shaft.

        :param data: Data used for calculating input shaft attributes.
        """
        self._calculator.calculate_preliminary_attributes()
        self._shaft_designer_controller.update_shaft_data(self._calculator.get_data())

    def _on_shaft_designing_finished(self):
        self._input_shaft.handle_shaft_designing_finished()

    def save_data(self):
        '''
        Get the component data
        '''
        data = []
        # Get calculator data
        data.append(self._calculator.get_data())

        # Get shaft designer data
        data.append(self._shaft_designer_controller.get_shaft_data())

        # Get every tab data
        for tab in self.tab_controllers[:-1]:
            data.append(tab.get_data())

        # Get is_shaft_designed flag
        data.append(self._input_shaft.is_shaft_designed)
        return data

    def load_data(self, data):
        '''
        Set the initial component data.
        '''
        # Set the calculators data
        self._calculator.set_data(data[0])

        # Set the shaft designer data
        if data[1]:
            self._shaft_designer_controller.update_shaft_data(self._calculator.get_data())
            self._shaft_designer_controller.set_shaft_data(data[1])

        # Set every tab data
        for idx, tab in enumerate(self.tab_controllers[:-1]):
            tab.set_state(data[idx+2])
        
        # Set is_shaft_designed_flag
        self._input_shaft.is_shaft_designed = data[-1]
        if self._input_shaft.is_shaft_designed:
            self._on_shaft_designing_finished()
