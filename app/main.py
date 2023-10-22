import sys
import os

root_directory = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(root_directory)

from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow
from MainWindowController import MainWindowController

def main():
    dbApp = QApplication([])

    mainWindow = MainWindow()
    mainWindowCtrl = MainWindowController(mainWindow)
    mainWindow.show()

    sys.exit(dbApp.exec())

if __name__ == "__main__":
    main()
