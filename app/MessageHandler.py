from PyQt6.QtWidgets import QMessageBox

from config import APP_NAME

class MessageHandler:
    _base_title = APP_NAME
    _icon = None

    @classmethod
    def _title(cls, title):
        return f"{cls._base_title} - {title}"

    @classmethod
    def critical(cls, parent, title, message):
        QMessageBox.critical(parent, cls._title(title), message)

    @classmethod
    def information(cls, parent, title, message):
        QMessageBox.information(parent, title, message)

    @classmethod
    def question(cls, parent, title, message):
        repsone = QMessageBox.question(parent, title, message)
        return repsone == QMessageBox.StandardButton.Yes