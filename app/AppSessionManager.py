import json
import os

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from AppWindow import AppWindow

class AppSessionManager:
    '''
    Manage saving and restoring the application progress, 
    '''
    def __init__(self, app_window: AppWindow):
        self._app_window = app_window

        self.current_file = ''
    
    def _save_data_to_file(self, file_path, data):
        if not file_path.endswith('.json'):
            file_path += '.json'
        
        try:
            with open(file_path, "w") as write_file:
                json.dump(data, write_file, indent=4)
        except Exception as e:
            self._show_message(QMessageBox.Icon.Critical, 'Błąd', f'Wystąpił błąd zapisywania pliku: {e}')
            return None

        self.current_file = file_path
        new_project_title = self._get_project_title(file_path)
        return new_project_title

    def save_data(self, suggested_file_name, data):
        if self.current_file:
            result = self._save_data_to_file(self.current_file, data)
        else:
            result = self.save_data_as(suggested_file_name, data)
        print(result)
        return result

    def save_data_as(self, suggested_file_name, data):
        file_path, _ = QFileDialog.getSaveFileName(self._app_window, 'Zapisz jako', suggested_file_name, 'JSON Files (*.json)')
        if file_path:
            return self._save_data_to_file(file_path, data)
        else:
            return None

    def load_data(self, load_data):
        data = None
        file_path = None
        file_dialog = QFileDialog(self._app_window, 'Otwórz', None, 'JSON Files (*.json)')

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, 'r') as read_file:
                    data = json.load(read_file)
                self._show_message(QMessageBox.Icon.Information, 'Dane Wczytane', 'Dane zostały wczytane.')
            except Exception as e:
                self._show_message(QMessageBox.Icon.Critical, 'Błąd', f'Wystąpił błąd podczas wczytywania pliku: {str(e)}')

        if data is None:
            return None
        else:
            try:
                load_data(data)
                new_project_title = self._get_project_title(file_path)
                return new_project_title
            except Exception as e:
                self._show_message(QMessageBox.Icon.Critical, 'Błąd', f'Wczytane dane są niepoprawne.')
                return None

    def _show_message(self, message_type, title, message):
        msg = QMessageBox(message_type, title, message, QMessageBox.StandardButton.Ok, self._app_window)
        msg.exec()

    def _get_project_title(self, file_path):
        return os.path.splitext(os.path.basename(file_path))[0]
