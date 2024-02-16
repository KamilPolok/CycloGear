from functools import partial

from PyQt6.QtCore import QTimer, QCoreApplication

from AppWindow import AppWindow, QuitDialog
from StartupWindow import StartupWindow

from AppSessionManager import AppSessionManager

from InputShaft.view.InputShaft import InputShaft
from InputShaft.controller.InputShaftController import InputShaftController
from InputShaft.model.InputShaftCalculator import InputShaftCalculator

class AppController():
    def __init__(self, app_window: AppWindow, launch_window: StartupWindow):
        self._app_window = app_window
        self._startup_window = launch_window

        self._app_initialized = False

        self._app_title = 'CycloGear2024'
        self._project_title = 'Projekt1'

        self._connect_signals_and_slots()
        self._startup()

        QTimer.singleShot(0, self._startup_window.exec)

    def _connect_signals_and_slots(self):
        self._app_window.save_action.triggered.connect(self._save_data)
        self._app_window.save_as_action.triggered.connect(self._save_data_as)
        self._app_window.quit_app_signal.connect(self._quit_app)

        self._startup_window.open_existing_project_signal.connect(partial(self._init_app, True))
        self._startup_window.create_new_project_signal.connect(partial(self._init_app, False))
        self._startup_window.quit_app_signal.connect(self._quit_app)

    def _startup(self):
        self._startup_window.setWindowTitle(self._app_title)
        self._set_app_window_title()
        self._app_window.show()

        self._session_manager = AppSessionManager(self._app_window)

        self._init_components()
    
    def _init_app(self, load_data):
        if load_data:
            result = self._load_data()
            if result:
                self._startup_window.accept()
                self._set_project_title(result)
                self._app_initialized = True
        else:
            self._app_initialized = True
    
    def _init_components(self):
        self._init_input_shaft_component()

    def _init_input_shaft_component(self):
        self._input_shaft = InputShaft()
        self._input_shaft_calculator = InputShaftCalculator()
        self._input_shaft_controller = InputShaftController(self._input_shaft_calculator, self._input_shaft)

        self._app_window.add_component(self._input_shaft)

    def _save_data(self):
        data = self._input_shaft_controller.save_data()
        result = self._session_manager.save_data(self._project_title, data)
        if result:
            self._set_project_title(result)
        print(result)
        return result

    def _save_data_as(self):
        data = self._input_shaft_controller.save_data()
        result = self._session_manager.save_data_as(self._project_title, data)
        if result:
            self._set_project_title(result)
        return result

    def _load_data(self):
        result = self._session_manager.load_data(self._input_shaft_controller.load_data)
        return result
        
    def _quit_app(self):
        if not self._app_initialized:
            QCoreApplication.quit()
            return
        
        dialog = QuitDialog(self._app_window)
        dialog.setWindowTitle(self._app_title)

        while True:
            result = dialog.exec()
            if result == QuitDialog.DialogCode.Accepted:
                if self._save_data():
                    QCoreApplication.quit()
                    break
            elif result == QuitDialog.DialogCode.Rejected:
                QCoreApplication.quit()
                break
            else:
                break

    def _set_app_window_title(self):
        self.window_title = self._app_title + ' - ' + self._project_title
        self._app_window.setWindowTitle(self.window_title)
    
    def _set_project_title(self, project_title):
        self._project_title = project_title
        self._set_app_window_title()
