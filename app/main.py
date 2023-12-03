import sys
import os

root_directory = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(root_directory)

from PyQt6.QtWidgets import QApplication

from MainWindow.view.MainWindow import MainWindow
from MainWindow.controller.MainWindowController import MainWindowController

def main():
    cyclo_app = QApplication([])

    data = {
        'nwe':[1500, 'obr/min'],
        'Ra':[None, 'N'],
        'Rb':[None, 'N'],
        'F': [5254.561, 'N'],
        'Mwe': [26.67, 'Nm'],
        'L': [80, 'mm'],
        'LA': [38, 'mm'],
        'LB': [75, 'mm'],
        'L1': [47, 'mm'],
        'L2': [64, 'mm'],
        'e': [10, 'mm'],
        'dsc': [None, 'mm'],
        'ds': [None, 'mm'],
        'dec': [None, 'mm'],
        'de': [None, 'mm'],
        'Materiał' : [None],
        'xz': [1, ''],
        'Łożyska_podporowe': [None],
        'Lhp': [10000, 'h'],
        'Lrp': [None, 'obr'],
        'Cr': [None, 'kN'],
        'fdp': [1.80, ''],
        'ftp': [1.00, ''],
        'Łożyska_centralne': [None],
        'Lhc': [10, 'h'],
        'Ltc': [None, 'obr'],
        'Cc': [None, 'kN'],
        'fdc': [1.00, ''],
        'ftc': [1.00, ''],
        }

    main_window = MainWindow()

    main_window_controller = MainWindowController(data, main_window)
    main_window.show()

    sys.exit(cyclo_app.exec())

if __name__ == "__main__":
    main()
