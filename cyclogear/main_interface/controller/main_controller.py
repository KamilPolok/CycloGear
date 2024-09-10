from PySide2.QtCore import QTimer, QCoreApplication

from ..view.MainWindow import MainWindow
from ..view.QuitDialog import QuitDialog
from ..view.StartupDialog import StartupDialog

from ..model.session_manager import SessionManager

from .startup_handler import StartupHandler

from input_mechanism.view.InputMechanism import InputMechanism
from input_mechanism.model.input_mechanism_calculator import InputMechanismCalculator
from input_mechanism.controller.input_mechanism_controller import InputMechanismController

from config import APP_NAME, INITIAL_PROJECT_NAME

class MainController():
    def __init__(self, app_window: MainWindow):
        self._app_window = app_window

        self._app_title = APP_NAME
        self._project_title = INITIAL_PROJECT_NAME

        self._session_manager = SessionManager(self._app_window)

        self._connect_signals_and_slots()

        QTimer.singleShot(0, self._startup)

    def _connect_signals_and_slots(self):
        self._app_window.saveAction.triggered.connect(self._save_data)
        self._app_window.saveAsAction.triggered.connect(self._save_data_as)
        self._app_window.quitAppSignal.connect(self._quit_app)

    def _startup(self):
        self._set_app_window_title()
        self._app_window.show()

        self._init_components()

        startup_window = StartupDialog(self._app_window)
        startup_handler = StartupHandler(startup_window, self._load_data)
        result = startup_handler.startup()

        if result:
            if startup_handler.new_project:
                self._init_components()
            else:
                self._set_project_title(startup_handler._project_title)
            self._startup_finished = True
            self._add_components()
        else:
            self._startup_finished = False
            self._app_window.close()

    def _init_components(self):
        self._components = []
        self._init_input_mechanism_component()

    def _add_components(self):
        for component in self._components:
            self._app_window.addComponent(component[0])

    def _load_data(self, data):
        for component in self._components:
            component[1].load_data(data)

    def _init_input_mechanism_component(self):
        self._input_mechanism = InputMechanism(self._app_window)
        self._input_mechanism_calculator = InputMechanismCalculator()
        self._input_mechanism_controller = InputMechanismController(self._input_mechanism_calculator, self._input_mechanism)
        self._components.append((self._input_mechanism, self._input_mechanism_controller))        

    def _save_data(self):
        data = self._input_mechanism_controller.save_data()
        result = self._session_manager.save_data(self._project_title, data)
        if result:
            self._set_project_title(result)
        return result

    def _save_data_as(self):
        data = self._input_mechanism_controller.save_data()
        result = self._session_manager.save_data_as(self._project_title, data)
        if result:
            self._set_project_title(result)
        return result
        
    def _quit_app(self):
        if not self._startup_finished:
            QCoreApplication.quit()
            return
            
        dialog = QuitDialog(self._app_window)

        while True:
            result = dialog.exec_()
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
