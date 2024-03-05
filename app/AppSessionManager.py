import json
import os

from PyQt6.QtWidgets import QFileDialog

from AppWindow import AppWindow
from Utility.MessageHandler import MessageHandler

class AppSessionManager:
    '''
    Manage saving and restoring the application progress, 
    '''
    def __init__(self, app_window: AppWindow):
        self._app_window = app_window

        self.current_file = ''
    
    def _get_project_title(self, file_path):
        return os.path.splitext(os.path.basename(file_path))[0]
    
    def _save_data_to_file(self, file_path, data):
        if not file_path.endswith('.json'):
            file_path += '.json'
        
        try:
            with open(file_path, "w") as write_file:
                json.dump(data, write_file, indent=4)
        except Exception as e:
            MessageHandler.critical(self._app_window, 'Błąd', f'Wystąpił błąd zapisywania pliku: {e}')
            return None

        self.current_file = file_path
        new_project_title = self._get_project_title(file_path)
        return new_project_title

    def save_data(self, suggested_file_name, data):
        if self.current_file:
            result = self._save_data_to_file(self.current_file, data)
        else:
            result = self.save_data_as(suggested_file_name, data)
        return result

    def save_data_as(self, suggested_file_name, data):
        file_path, _ = QFileDialog.getSaveFileName(self._app_window, 'Zapisz jako', suggested_file_name, 'JSON Files (*.json)')
        if file_path:
            return self._save_data_to_file(file_path, data)
        else:
            return None
