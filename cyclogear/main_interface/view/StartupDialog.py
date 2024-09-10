from PySide2.QtWidgets import QDialog, QVBoxLayout
from PySide2.QtCore import Signal, Qt

from .MainWindow import MainWindow

from utils.widgets.PushButton import PushButton
from config import APP_NAME

class StartupDialog(QDialog):
    '''
    Views window on startup of the application,
    where user can select actions to perform -
    create new project, open existing project
    or quit.
    '''
    newProjectSignal = Signal()
    openProjectSignal = Signal()
    quitAppSignal = Signal()
    
    def __init__(self, parent: MainWindow):
        super().__init__(parent)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint)

        self._initUI()
    
    def _initUI(self):
        self.setFixedSize(200, 120)

        layout = QVBoxLayout(self)
        
        newButton = PushButton("Nowy Projekt", self)
        newButton.clicked.connect(self.newProjectSignal.emit)
        
        openButton = PushButton("Otwórz Projekt", self)
        openButton.clicked.connect(self.openProjectSignal.emit)

        exitButton = PushButton("Wyjdź", self)
        exitButton.clicked.connect(self.quitAppSignal.emit)
        
        layout.addWidget(newButton)
        layout.addWidget(openButton)
        layout.addWidget(exitButton)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)
