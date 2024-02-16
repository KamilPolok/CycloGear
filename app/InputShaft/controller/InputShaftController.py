from InputShaft.Mediator import Mediator
from InputShaft.view.InputShaft import InputShaft
from InputShaft.model.InputShaftCalculator import InputShaftCalculator

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
        self._input_shaft.set_data(self._calculator.get_data())
        self._input_shaft.init_tabs()

        self._mediator = Mediator()
        self._init_shaft_designer()

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

        self._input_shaft.tabs[0].select_material_button.clicked.connect(self._on_select_materials)
        self._input_shaft.tabs[0].update_data_signal.connect(self._update_input_shaft_attributes)

        self._input_shaft.tabs[1].select_support_A_bearing_signal.connect(self._on_select_support_A_bearing)
        self._input_shaft.tabs[1].select_support_B_bearing_signal.connect(self._on_select_support_B_bearing)
        self._input_shaft.tabs[1].select_central_bearing_signal.connect(self._on_select_central_bearing)
        self._input_shaft.tabs[1].update_data_signal.connect(self._on_update_bearings_data)

        self._input_shaft.tabs[2].select_support_A_bearing_rolling_element_signal.connect(self._on_select_support_A_bearing_rolling_element)
        self._input_shaft.tabs[2].select_support_B_bearing_rolling_element_signal.connect(self._on_select_support_B_bearing_rolling_element)
        self._input_shaft.tabs[2].select_central_bearing_rolling_element_signal.connect(self._on_select_central_bearing_rolling_element)
        self._input_shaft.tabs[2].update_data_signal.connect(self._on_update_power_loss_data)

    def _open_shaft_designer_window(self):
        if self._shaft_designer.isHidden():
            self._shaft_designer.show()

    def _on_select_materials(self):
        self._calculator.open_shaft_material_selection(self._input_shaft.tabs[0].update_selected_material)

    def _on_select_support_A_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_support_A_bearing_load_capacity()
        self._calculator.open_support_A_bearing_selection(self._input_shaft.tabs[1].update_selected_support_A_bearing)

    def _on_select_support_B_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_support_B_bearing_load_capacity()
        self._calculator.open_support_B_bearing_selection(self._input_shaft.tabs[1].update_selected_support_B_bearing)

    def _on_select_central_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_central_bearing_load_capacity()
        self._calculator.open_central_bearing_selection(self._input_shaft.tabs[1].update_selected_central_bearing)

    def _on_update_bearings_data(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_bearings_attributes()

    def _on_select_support_A_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_support_A_bearing_rolling_element_selection(self._input_shaft.tabs[2].update_selected_support_A_bearing_rolling_element)
            
    def _on_select_support_B_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_support_B_bearing_rolling_element_selection(self._input_shaft.tabs[2].update_selected_support_B_bearing_rolling_element)
            
    def _on_select_central_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_central_bearing_rolling_element_selection(self._input_shaft.tabs[2].update_selected_central_bearing_rolling_element)

    def _on_update_power_loss_data(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_bearings_power_loss()
         
    def _update_input_shaft_attributes(self, data):
        """
        Calculate attributes for the input shaft.

        :param data: Data used for calculating input shaft attributes.
        """
        self._calculator.update_data(data)
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
        for tab in self._input_shaft.tabs[:-1]:
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
        for idx, tab in enumerate(self._input_shaft.tabs[:-1]):
            tab.set_tab(data[idx+2])
        
        # Set is_shaft_designed_flag
        self._input_shaft.is_shaft_designed = data[-1]
        if self._input_shaft.is_shaft_designed:
            self._on_shaft_designing_finished()
