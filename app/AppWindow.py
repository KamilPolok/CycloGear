from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction, QIcon

from config import APP_NAME, APP_ICON


class AppWindow(QMainWindow):
    '''
    Sets the basic User Interface and access point to 
    functionalities, also views the app components that can be 
    added through add_component() method.
    '''
    quit_app_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        '''
        Set user interface.
        '''
        # Set window icon
        self.setWindowIcon(QIcon(APP_ICON))
        # Set window size
        self.resize(800,500)

        # Set layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

        # Set menu bar
        self._set_menu_bar()

    def _set_menu_bar(self):
        '''
        Set menu bar and add actions to it.
        '''
        # Set menu bar
        menu_bar = self.menuBar()

        # Set the "File" menu and add it to the menu bar
        file_menu = menu_bar.addMenu('&Plik')

        # Set the "Save" action
        self.save_action = QAction('&Zapisz', self)
        self.save_action.setStatusTip("Ctrl + S")
        self.save_action.setShortcut("Ctrl+S")

        # Set the "Save as" action
        self.save_as_action = QAction('&Zapisz jako', self)
        self.save_as_action.setStatusTip("Ctrl + Shift + S")
        self.save_as_action.setShortcut("Ctrl+Shift+S")

        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)

    def closeEvent(self, event):
        '''
        Overload closeEvent to emit signal that triggers
        additional methods that need be performed on app shutdown.
        '''
        self.quit_app_signal.emit()
        event.ignore()

    def add_component(self, component: QWidget):
        '''
        Add component to the window.
        '''
        self.main_layout.addWidget(component)

class QuitDialog(QDialog):
    '''
    Dialog Window opened on closing the app window.
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(APP_NAME)
        # Disable close, minimize, window buttons
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Zapisać zmiany w projekcie?", self)
        self.layout.addWidget(self.label)

        # Create the QDialogButtonBox with Yes and No buttons
        self.button_box = QDialogButtonBox()
        self.button_box.addButton(QDialogButtonBox.StandardButton.Yes)
        self.button_box.addButton(QDialogButtonBox.StandardButton.No)

        # Add a custom "Ignore" button
        self.ignore_button = self.button_box.addButton("Anuluj", QDialogButtonBox.ButtonRole.RejectRole)

        # Customize button texts
        self.button_box.button(QDialogButtonBox.StandardButton.Yes).setText("Zapisz zmiany")
        self.button_box.button(QDialogButtonBox.StandardButton.No).setText("Odrzuć zmiany")

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.ignore_button.clicked.connect(self.ignore)

        self.layout.addWidget(self.button_box)

    def ignore(self):
        self.done(2)  # Custom return code for "Ignore" button
