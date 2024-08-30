from ..mediator import Mediator

from ..model.input_shaft_calculator import InputShaftCalculator
from ..view.InputShaft import InputShaft

from ..tabs.drive_shaft_tab.view.DriveShaftTab import DriveShaftTab
from ..tabs.drive_shaft_tab.model.drive_shaft_tab_calculator import DriveShaftTabCalculator
from ..tabs.drive_shaft_tab.controller.drive_shaft_tab_controller import DriveShaftTabController

from ..tabs.bearings_tab.view.BearingsTab import BearingsTab
from ..tabs.bearings_tab.model.bearings_tab_calculator import BearingsTabCalculator
from ..tabs.bearings_tab.controller.bearings_tab_controller import BearingsTabController

from ..tabs.power_loss_tab.view.PowerLossTab import PowerLossTab
from ..tabs.power_loss_tab.model.power_loss_calculator import PowerLossTabCalculator
from ..tabs.power_loss_tab.controller.power_loss_controller import PowerLossTabController

from ..tabs.results_tab.view.ResultsTab import ResultsTab
from ..tabs.results_tab.controller.results_tab_controller import ResultsTabController

from shaft_designer.view.ShaftDesigner import ShaftDesigner
from shaft_designer.controller.shaft_designer_controller import ShaftDesignerController

from db_handler.controller.db_controller import ViewSelectItemController
from db_handler.model.db_handler import DbHandler
from db_handler.view.Window import Window

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
        self._calculator.set_initial_data()
        self._initTabs()
        self._init_shaft_designer()

    def _initTabs(self):
        tab_id = 1

        tab1 = DriveShaftTab(self._input_shaft)
        tab1_calculator = DriveShaftTabCalculator()
        tab1_controller = DriveShaftTabController(tab_id, tab1, tab1_calculator, self._mediator)

        tab_id +=1
        tab2 = BearingsTab(self._input_shaft)
        tab2_calculator = BearingsTabCalculator()
        tab2_controller = BearingsTabController(tab_id, tab2, tab2_calculator, self._mediator)

        tab_id +=1
        tab3 = PowerLossTab(self._input_shaft)
        tab3_calculator = PowerLossTabCalculator()
        tab3_controller = PowerLossTabController(tab_id, tab3, tab3_calculator, self._mediator)

        tab_id +=1
        tab4 = ResultsTab(self._input_shaft)
        tab4_controller = ResultsTabController(tab_id, tab4, self._mediator)

        self.tabs = [tab1, tab2, tab3, tab4]
        self.tab_controllers = [tab1_controller, tab2_controller, tab3_controller, tab4_controller]
        tab_titles = ['Wał Czynny', 'Łożyska', 'Straty Mocy', 'Wyniki']

        for tab_controller in self.tab_controllers:
            data = self._calculator.get_data()
            tab_controller.init_state(data)

        self._input_shaft.initTabs(self.tabs, tab_titles)

    def _init_shaft_designer(self):
        # Set an instance of shaft designer
        window_title = 'Wał Czynny'
        self._shaft_designer = ShaftDesigner(window_title)

        # Set an instance of shaft designer controller
        self._shaft_designer_controller = ShaftDesignerController(self._shaft_designer, self._mediator)

    def _connect_signals_and_slots(self):
        """
        Connect signals and slots for interactivity in the application.

        This method sets up connections between UI elements and their corresponding
        actions or handlers.
        """
        self._input_shaft.previewButton.clicked.connect(self._open_shaft_designer_window)
        self._mediator.shaftDesigningFinished.connect(self._on_shaft_designing_finished)

        self._mediator.selectMaterial.connect(self._on_select_materials)
        self._mediator.selectBearing.connect(self._on_select_bearing)
        self._mediator.selectRollingElement.connect(self._on_select_rolling_element)

        self._mediator.updateComponentData.connect(self._update_component_data)

        self._mediator.bearingChanged.connect(self._on_bearing_changed)

    def _update_component_data(self, tab_id, data):
        self._calculator.update_data(data)

        if tab_id == 1:
            self._on_update_preliminary_data()
        elif tab_id == 2:
            self._on_update_bearings_data()
        elif tab_id == 3:
            self._on_update_power_loss_data()

    def _open_shaft_designer_window(self):
        self._shaft_designer.show()

    def _on_select_materials(self):
        result = self._open_shaft_material_selection()
        if result:
            self.tab_controllers[0].on_materials_selected(result)

    def _on_select_bearing(self, bearing_section_id, data):
        self._calculator.update_data(data)
        result = self._open_bearing_selection(bearing_section_id)
        if result:
            self.tab_controllers[1].on_bearing_selected(bearing_section_id, result)

    def _on_select_rolling_element(self, bearing_section_id, data):
        self._calculator.update_data(data)
        result = self._open_rolling_element_selection(bearing_section_id)
        if result:
            self.tab_controllers[2].on_rolling_element_selected(bearing_section_id, result)

    def _on_update_preliminary_data(self):
        """
        Calculate attributes for the input shaft.

        :param data: Data used for calculating input shaft attributes.
        """
        self._shaft_designer_controller.update_shaft_data(self._calculator.get_data())

    def _on_update_bearings_data(self):
        self._calculator.calculate_bearings_attributes()

    def _on_update_power_loss_data(self):
        self._calculator.calculate_absolute_power_loss()

    def _on_bearing_changed(self, bearing_section_id, bearing_data):
        bearing_data = self._calculator.get_bearing_attributes(bearing_section_id, bearing_data)
        self._shaft_designer_controller.update_bearing_data(bearing_data)

    def _on_shaft_designing_finished(self):
        self._input_shaft.handleShaftDesigningFinished()

    def _open_shaft_material_selection(self):
        """
        Open the window for selection of the shaft material

        Returns:
            (None or dict): selected item data.
        """
        db_handler = DbHandler()
        db_window = Window(self._input_shaft)
        db_window.setWindowTitle("Dobór materiału")
        tables_group_name = 'wał czynny-materiały'

        available_tables = db_handler.get_available_tables(tables_group_name)
        limits = db_handler.get_table_items_filters(tables_group_name)
        view_select_items_ctrl = ViewSelectItemController(db_handler, db_window, available_tables, limits)
        result = view_select_items_ctrl.startup()
        if result:
            return view_select_items_ctrl.selected_item_attributes
        else:
            return None
        
    def _open_bearing_selection(self, bearing_section_id):
        """
        Open the window for bearing selection the.

        Args:
            bearing_section_id (str): Id of section that specifies the bearing location.

        Returns:
            (None or dict): selected item data.
        """
        # Specify the name of the tables to open
        if bearing_section_id == 'support_A' or  bearing_section_id == 'support_B':
            tables_group_name = 'wał czynny-łożyska-podporowe'
        elif bearing_section_id == 'eccentrics':
            tables_group_name = 'wał czynny-łożyska-centralne'

        db_handler = DbHandler()
        db_window = Window(self._input_shaft)
        db_window.setWindowTitle("Dobór łożyska")
        # Get available tables
        available_tables = db_handler.get_available_tables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.get_table_items_filters(tables_group_name)
        self._calculator.set_bearings_attributes_limits(limits, bearing_section_id)
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, db_window, available_tables, limits)
        result = view_select_items_ctrl.startup()
        if result:
            return view_select_items_ctrl.selected_item_attributes
        else:
            return None
        
    def _open_rolling_element_selection(self, bearing_section_id):
        """
        Open the window for rolling element selection.

        Args:
            bearing_section_id (str): Id of section that specifies the bearing location for which the rollin 
                                      elements are being selected.
        Returns:
            (None or dict): selected item data.
        """
        db_handler = DbHandler()
        db_window = Window(self._input_shaft)
        db_window.setWindowTitle("Dobór elementu tocznego")
        # Get available tables
        tables_group_name = f"wał czynny-elementy toczne-{self._calculator.get_bearing_rolling_element_type(bearing_section_id)}"
        available_tables = db_handler.get_available_tables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.get_table_items_filters(tables_group_name)
        self._calculator.set_rollings_element_limits(limits, bearing_section_id)
        
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, db_window, available_tables, limits)
        result = view_select_items_ctrl.startup()
        if result:
            return view_select_items_ctrl.selected_item_attributes
        else:
            return None

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
        for tab_controller in self.tab_controllers[:-1]:
            data.append(tab_controller.get_data())

        # Get isShaftDesigned flag
        data.append(self._input_shaft.isShaftDesigned)
        return data

    def load_data(self, data):
        '''
        Set the initial component data.
        '''
        # Set the calculators data
        self._calculator.set_data(data[0])
        self._calculator.set_initial_data()

        # Set the shaft designer data
        if data[1]:
            self._shaft_designer_controller.update_shaft_data(self._calculator.get_data())
            self._shaft_designer_controller.set_shaft_data(data[1])

        # Set every tab data
        for idx, tab_controller in enumerate(self.tab_controllers[:-1]):
            tab_controller.set_state(data[idx+2])
        
        # Set isShaftDesigned flag
        self._input_shaft.isShaftDesigned = data[-1]
        if self._input_shaft.isShaftDesigned:
            self._on_shaft_designing_finished()
