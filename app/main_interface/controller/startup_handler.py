
import json
import os

from PyQt6.QtWidgets import QFileDialog

from ..view.StartupDialog import StartupDialog
from utils.message_handler import MessageHandler

class StartupHandler():
    def __init__(self, startup_window: StartupDialog, load_data_to_components: callable):
        self._startup_window = startup_window
        self._try_to_load_data_to_components = load_data_to_components

        self._connect_signals_and_slots()
    
    def _connect_signals_and_slots(self):
        self._startup_window.quitAppSignal.connect(self._startup_window.reject)
        self._startup_window.newProjectSignal.connect(self._startup_window.accept)       
        self._startup_window.openProjectSignal.connect(self._load_data)

    def _load_data(self):
        data = self._load_json_data()

        result = self._is_data_valid(data)
        if result:
            self.new_project = False
            self._project_title = self._get_project_title(self.file_path)
            self._startup_window.accept()

    def _load_json_data(self):
        data = []
        file_dialog = QFileDialog(self._startup_window, 'Otwórz', None, 'JSON Files (*.json)')
        if file_dialog.exec():
            self.file_path = file_dialog.selectedFiles()[0]
            try:
                with open(self.file_path, 'r') as read_file:
                    data = json.load(read_file)
                MessageHandler.information(self._startup_window, 'Dane Wczytane', 'Dane zostały wczytane.')
            except Exception as e:
                MessageHandler.critical(self._startup_window, 'Błąd wczytywania', f'Wystąpił błąd podczas wczytywania pliku: {str(e)}')
        
        return data

    def _is_data_valid(self, data):
        if not data:
            return False
        try:
            self._try_to_load_data_to_components(data)
            return True
        except Exception as e:
            MessageHandler.critical(self._startup_window, 'Nieprawidłowe dane', f'Wczytane dane są niepoprawne.')
            return False

    def _get_project_title(self, file_path):
        return os.path.splitext(os.path.basename(file_path))[0]
    
    def startup(self):
        self.new_project = True
        result = self._startup_window.exec()
        return result == self._startup_window.DialogCode.Accepted
