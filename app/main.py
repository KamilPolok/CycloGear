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
        'nwe':[1500, 'obr/min'],
        'Ra':[None, 'obr/min'],
        'Rb':[None, 'obr/min'],
        'F1': [100, 'N'],
        'F2': [-100, 'N'],
        'Mo': [9.55, 'Nm'],
        'L': [None, 'mm'],
        'LA': [None, 'mm'],
        'LB': [None, 'mm'],
        'L1': [None, 'mm'],
        'L2': [None, 'mm'],
        'e': [10, 'mm'],
        'ds': [None, 'mm'],
        'de': [None, 'mm'],
        'Materiał' : [None],
        'xz': [None, ''],
        'Łożyska1': [None],
        'Lh1': [None, 'h'],
        'Lt1': [None, ''],
        'C1': [None, ''],
        'fd1': [None, ''],
        'ft1': [None, ''],
        'Łożyska2': [None],
        'Lh2': [None, 'h'],
        'Lt2': [None, ''],
        'C2': [None, ''],
        'fd2': [None, ''],
        'ft2': [None, ''],
        }

    mainWindow = MainWindow()

    mainWindowCtrl = MainWindowController(data, mainWindow)
    mainWindow.show()

    sys.exit(dbApp.exec())

if __name__ == "__main__":
    main()
