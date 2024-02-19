
import json
import os
from functools import partial 

from PyQt6.QtWidgets import QFileDialog

from StartupWindow import StartupWindow
from MessageHandler import MessageHandler 

class StartupHandler():
    def __init__(self, app_name, startup_window: StartupWindow):
        self._startup_window = startup_window
        self._startup_window.setWindowTitle(app_name)

        self._connect_signals_and_slots()
    
    def _connect_signals_and_slots(self):
        self._startup_window.quit_app_signal.connect(self._quit_app)
        self._startup_window.open_existing_project_signal.connect(self._load_data)
        self._startup_window.create_new_project_signal.connect(partial(self._finish_startup, ()))
        
    def _quit_app(self):
        self._startup_window.reject()

    def _finish_startup(self, data):
        self.data = data
        self._startup_window.accept()       

    def _load_data(self):
        data = None
        file_path = None
        while True:
            file_dialog = QFileDialog(self._startup_window, 'Otwórz', None, 'JSON Files (*.json)')
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
                try:
                    with open(file_path, 'r') as read_file:
                        data = json.load(read_file)
                    MessageHandler.information(self._startup_window, 'Dane Wczytane', 'Dane zostały wczytane.')
                    break  # Break the loop if data is loaded successfully
                except Exception as e:
                    MessageHandler.critical(self._startup_window, 'Błąd', f'Wystąpił błąd podczas wczytywania pliku: {str(e)}')
                    # The loop will continue, prompting the user to select a file again
            else:
                # If the user cancels the dialog, return without trying to load data
                return

        existing_project_title = self._get_project_title(file_path)

        self._finish_startup((data, existing_project_title))

    def _get_project_title(self, file_path):
        return os.path.splitext(os.path.basename(file_path))[0]
    
    def get_data(self):
        return self.data