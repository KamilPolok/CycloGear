from AppWindow import AppWindow

from InputShaft.view.InputShaft import InputShaft
from InputShaft.controller.InputShaftController import InputShaftController
from InputShaft.model.InputShaftCalculator import InputShaftCalculator

class AppController():
    def __init__(self, data, app_window: AppWindow):
        self._data = data
        self._app_window = app_window
        self._init_input_shaft_component()
    
    def _init_input_shaft_component(self):
        self._input_shaft = InputShaft()
        self._input_shaft_calculator = InputShaftCalculator(self._data)
        self._input_shaft_controller = InputShaftController(self._input_shaft_calculator, self._input_shaft)

        self._app_window.add_component(self._input_shaft)
