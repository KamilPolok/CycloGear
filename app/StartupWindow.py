from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

from AppWindow import AppWindow

class StartupWindow(QDialog):
    '''
    Views widnow on startup of the application,
    where user can select actions to perfrom -
    create new project, open existing project
    or quit.
    '''
    create_new_project_signal = pyqtSignal()
    open_existing_project_signal = pyqtSignal()
    quit_app_signal = pyqtSignal()
    
    def __init__(self, parent: AppWindow):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint)

        self._init_ui()
    
    def _init_ui(self):
        self.setFixedSize(200, 100)

        layout = QVBoxLayout(self)
        
        new_button = QPushButton("Nowy Projekt", self)
        new_button.clicked.connect(self.create_new_project)
        
        open_button = QPushButton("Otwórz Projekt", self)
        open_button.clicked.connect(self.open_existing_project)

        exitButton = QPushButton("Wyjdź", self)
        exitButton.clicked.connect(self.close_app)
        
        layout.addWidget(new_button)
        layout.addWidget(open_button)
        layout.addWidget(exitButton)

    def create_new_project(self):
        self.create_new_project_signal.emit()
    
    def open_existing_project(self):
        self.open_existing_project_signal.emit()

    def close_app(self):
        self.quit_app_signal.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)
