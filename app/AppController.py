from PyQt6.QtCore import QTimer, QCoreApplication

from MessageHandler import MessageHandler
from AppWindow import AppWindow, QuitDialog

from StartupHandler import StartupHandler
from StartupWindow import StartupWindow

from AppSessionManager import AppSessionManager

from InputShaft.view.InputShaft import InputShaft
from InputShaft.controller.InputShaftController import InputShaftController
from InputShaft.model.InputShaftCalculator import InputShaftCalculator

class AppController():
    def __init__(self, app_window: AppWindow):
        self._app_window = app_window

        self._app_title = 'CycloGear2024'
        self._project_title = 'Projekt1'

        self._session_manager = AppSessionManager(self._app_window)
        MessageHandler.set_attributes(self._app_title)

        self._connect_signals_and_slots()

        QTimer.singleShot(0, self._startup)

    def _connect_signals_and_slots(self):
        self._app_window.save_action.triggered.connect(self._save_data)
        self._app_window.save_as_action.triggered.connect(self._save_data_as)
        self._app_window.quit_app_signal.connect(self._quit_app)

    def _startup(self):
        self._set_app_window_title()
        self._app_window.show()

        self._startup_finished = False
        startup_window = StartupWindow(self._app_window)
        startup_handler = StartupHandler(self._app_title, startup_window)

        while not self._startup_finished:
            self._init_components()
            result = startup_window.exec()
            if result == StartupWindow.DialogCode.Accepted:
                data = startup_handler.get_data()
                if data:
                    project_data, project_title = data
                    result = self._load_data(project_data)
                    if result:
                        self._startup_finished = True
                        self._set_project_title(project_title)
                else:
                    self._startup_finished = True
            else:
                break

        if self._startup_finished:
            self._add_components()
        else:
            self._quit_app()

    def _init_components(self):
        self._components = []
        self._init_input_shaft_component()

    def _add_components(self):
        for component in self._components:
            self._app_window.add_component(component)

    def _init_input_shaft_component(self):
        self._input_shaft = InputShaft()
        self._input_shaft_calculator = InputShaftCalculator()
        self._input_shaft_controller = InputShaftController(self._input_shaft_calculator, self._input_shaft)
        self._components.append(self._input_shaft)

    def _load_data(self, data):
        if data == None:
            return False
        try:
            self._input_shaft_controller.load_data(data)
            return True
        except Exception as e:
            MessageHandler.critical(self._app_window, 'Błąd', f'Wczytane dane są niepoprawne.')
            return False

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
        
    def _quit_app(self):
        if not self._startup_finished:
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
