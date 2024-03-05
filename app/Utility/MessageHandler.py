from PyQt6.QtWidgets import QMessageBox, QWidget

from config import APP_NAME

class MessageHandler:
    """
    Class for displying windows with information, critical
    message or question. This class is not meant to be instantiated.
    """
    _base_title = APP_NAME
    _icon = None

    def __new__(cls, *args, **kwargs):
        raise TypeError("This class cannot be instantiated")

    @classmethod
    def _title(cls, subtitle: str) -> str:
        """
        Concatenate the bas title with the subtitle

        Args:
            subtitle (str): additional window description
        """
        return f"{cls._base_title} - {subtitle}"

    @classmethod
    def critical(cls, parent: QWidget, title: str, message: str):
        """
        Show critical message.

        Args:
            parent (QWidget): Parent (UI) of the message box.
            title (str): Description added to window title.
            message (str): Message to display.
        """
        QMessageBox.critical(parent, cls._title(title), message)

    @classmethod
    def information(cls, parent: QWidget, title: str, message: str):
        """
        Show information message.

        Args:
            parent (QWidget): Parent (UI) of the message box.
            title (str): Description added to window title.
            message (str): Message to display.
        """
        QMessageBox.information(parent, cls._title(title), message)

    @classmethod
    def question(cls, parent: QWidget, title: str, message: str) -> bool:
        """
        Show question.

        Args:
            parent (QWidget): Parent (UI) of the message box.
            title (str): Description added to window title.
            message (str): Message to display.
        Returns:
            (bool): response of the user (yes = True, no = False)
        """
        response = QMessageBox.question(parent, cls._title(title), message)
        return response == QMessageBox.StandardButton.Yes
