from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from config import APP_NAME

class QuitDialog(QDialog):
    '''
    Dialog Window opened on closing the app window.
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(APP_NAME)

        # Disable close, minimize, window buttons
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint)

        self.layout = QVBoxLayout(self)

        self._set_message()
        self._set_buttons()

    def _set_message(self):
        self.label = QLabel("Zapisać zmiany w projekcie?", self)
        self.layout.addWidget(self.label)

    def _set_buttons(self):
        # Buttons layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(10)
        self.layout.addLayout(buttonLayout)

        # Yes Button
        self.yesButton = QPushButton("Tak")
        buttonLayout.addWidget(self.yesButton)
        self.yesButton.setFixedWidth(80)
        self.yesButton.clicked.connect(self.accept)

        # No button
        self.noButton = QPushButton("Nie")
        self.noButton.setFixedWidth(80)
        self.noButton.clicked.connect(self.reject)
        buttonLayout.addWidget(self.noButton)

        # Ignore Button
        self.ignoreButton = QPushButton("Anuluj")
        buttonLayout.addWidget(self.ignoreButton)
        self.ignoreButton.setFixedWidth(80)
        self.ignoreButton.clicked.connect(self.ignore)

        # Install event filter to catch key presses
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        # Check if the event is a key press event
        if event.type() == QKeyEvent.Type.KeyPress:
            # Check if the key is the Esc key
            if event.key() == Qt.Key.Key_Escape:
                # Ignore the dialog instead of rejecting it
                self.ignore()
                return True  # Indicate that the event has been handled
        return super().eventFilter(obj, event)

    def ignore(self):
        self.done(2)  # Custom return code for "Ignore" button
