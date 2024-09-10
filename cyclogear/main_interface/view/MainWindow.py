from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QAction
from PySide2.QtCore import Signal 
from PySide2.QtGui import QIcon

from config import APP_ICON

class MainWindow(QMainWindow):
    '''
    Sets the basic User Interface and access point to 
    functionalities, also views the app components that can be 
    added through addComponent() method.
    '''
    quitAppSignal = Signal()

    def __init__(self):
        super().__init__()

        self._initUI()

    def _initUI(self):
        '''
        Set user interface.
        '''
        # Set window icon
        self.setWindowIcon(QIcon(APP_ICON))
        # Set window size
        self.resize(800, 500)

        # Set layout
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        # Set menu bar
        self._setMenuBar()

    def _setMenuBar(self):
        '''
        Set menu bar and add actions to it.
        '''
        # Set menu bar
        menuBar = self.menuBar()

        # Set the "File" menu and add it to the menu bar
        fileMenu = menuBar.addMenu('&Plik')

        # Set the "Save" action
        self.saveAction = QAction('&Zapisz', self)
        self.saveAction.setStatusTip("Ctrl + S")
        self.saveAction.setShortcut("Ctrl+S")

        # Set the "Save as" action
        self.saveAsAction = QAction('&Zapisz jako', self)
        self.saveAsAction.setStatusTip("Ctrl + Shift + S")
        self.saveAsAction.setShortcut("Ctrl+Shift+S")

        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)

    def closeEvent(self, event):
        '''
        Overload closeEvent to emit signal that triggers
        additional methods that need be performed on app shutdown.
        '''
        self.quitAppSignal.emit()
        event.ignore()

    def addComponent(self, component: QWidget):
        '''
        Add component to the window.
        '''
        self.mainLayout.addWidget(component)
