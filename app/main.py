import sys
import os

root_directory = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(root_directory)

from PyQt6.QtWidgets import QApplication

from MainWindow import MainWindow
from MainWindowController import MainWindowController

def main():
    dbApp = QApplication([])

    data = {
        'F1': [100, 'N'],
        'F2': [-100, 'N'],
        'Mo': [9.55, 'Nm'],
        'L': [None, 'mm'],
        'LA': [None, 'mm'],
        'LB': [None, 'mm'],
        'L1': [None, 'mm'],
        'L2': [None, 'mm'],
        'e': [10, 'mm'],
        'xz': [None, '']
        }

    mainWindow = MainWindow()

    mainWindowCtrl = MainWindowController(data, mainWindow)
    mainWindow.show()

    sys.exit(dbApp.exec())

if __name__ == "__main__":
    main()
