from PyQt6.QtWidgets import QMessageBox

class MessageHandler:
    _base_title = ''
    _icon = None

    @classmethod
    def _title(cls, title):
        return f"{cls._base_title} - {title}" if cls._base_title else title

    @classmethod
    def set_attributes(cls, title):
        cls._base_title = title

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