import sys

import Utility.path_config

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication

from AppWindow import AppWindow

from AppController import AppController

def on_about_to_quit():
    # Perform necessary checks or operations
    QCoreApplication.processEvents()

def main():
    cyclo_app = QApplication([])
    cyclo_app.aboutToQuit.connect(on_about_to_quit)

    app_window = AppWindow()

    app_controller = AppController(app_window)

    sys.exit(cyclo_app.exec())

if __name__ == "__main__":

    main()
