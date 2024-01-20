from AppWindow import AppWindow

from MainWindow.view.MainWindow import MainWindow
from MainWindow.controller.MainWindowController import MainWindowController

class AppController():
    def __init__(self, data, app_window: AppWindow):
        self._data = data
        self._app_window = app_window
        self._init_main_window_component()
    
    def _init_main_window_component(self):
        self._main_window = MainWindow()
        self._main_window_controller = MainWindowController(self._data, self._main_window)

        self._app_window.add_component(self._main_window)
