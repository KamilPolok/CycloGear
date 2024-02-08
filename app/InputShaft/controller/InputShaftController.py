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
        self._input_shaft.tabs[0].updated_data_signal.connect(self._update_input_shaft_attributes)

        self._input_shaft.tabs[1].updated_support_A_bearing_data_signal.connect(self._on_select_support_A_bearing)
        self._input_shaft.tabs[1].updated_support_B_bearing_data_signal.connect(self._on_select_support_B_bearing)
        self._input_shaft.tabs[1].updated_central_bearing_data_signal.connect(self._on_select_central_bearing)
        self._input_shaft.tabs[1].updated_data_signal.connect(self._on_update_bearings_data)

        self._input_shaft.tabs[2].updated_support_A_bearing_rolling_element_data_signal.connect(self._on_select_support_A_bearing_rolling_element)
        self._input_shaft.tabs[2].updated_support_B_bearing_rolling_element_data_signal.connect(self._on_select_support_B_bearing_rolling_element)
        self._input_shaft.tabs[2].updated_central_bearing_rolling_element_data_signal.connect(self._on_select_central_bearing_rolling_element)
        self._input_shaft.tabs[2].updated_data_signal.connect(self._on_update_power_loss_data)

    def _open_shaft_designer_window(self):
        if self._shaft_designer.isHidden():
            self._shaft_designer.show()

    def _on_select_materials(self):
        self._calculator.open_shaft_material_selection(self._input_shaft.tabs[0].update_viewed_material)

    def _on_select_support_A_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_support_A_bearing_load_capacity()
        self._calculator.open_support_A_bearing_selection(self._input_shaft.tabs[1].update_viewed_support_A_bearing_code)

    def _on_select_support_B_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_support_B_bearing_load_capacity()
        self._calculator.open_support_B_bearing_selection(self._input_shaft.tabs[1].update_viewed_support_B_bearing_code)

    def _on_select_central_bearing(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_central_bearing_load_capacity()
        self._calculator.open_central_bearing_selection(self._input_shaft.tabs[1].update_viewed_central_bearings_code)

    def _on_update_bearings_data(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_bearings_attributes()

    def _on_select_support_A_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_support_A_bearing_rolling_element_selection(self._input_shaft.tabs[2].update_viewed_support_A_bearings_rolling_element_code)
            
    def _on_select_support_B_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_support_B_bearing_rolling_element_selection(self._input_shaft.tabs[2].update_viewed_support_B_bearings_rolling_element_code)
            
    def _on_select_central_bearing_rolling_element(self, data):
        self._calculator.update_data(data)
        self._calculator.open_central_bearing_rolling_element_selection(self._input_shaft.tabs[2].update_viewed_central_bearings_rolling_element_code)

    def _on_update_power_loss_data(self, data):
        self._calculator.update_data(data)
        self._calculator.calculate_bearings_power_loss()
         
    def _update_input_shaft_attributes(self, data):
        """
        Calculate attributes for the input shaft.

        :param data: Data used for calculating input shaft attributes.
        """
        self._calculator.update_data(data)
        self._shaft_designer_controller.update_shaft_data(self._calculator.get_data())

    def _on_shaft_designing_finished(self):
        self._input_shaft.handle_shaft_designing_finished()
