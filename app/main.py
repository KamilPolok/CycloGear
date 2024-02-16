import sys

import Utility.path_config

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication

from AppWindow import AppWindow
from StartupWindow import StartupWindow

from AppController import AppController

def on_about_to_quit():
    # Perform necessary checks or operations
    QCoreApplication.processEvents()

def main():
    cyclo_app = QApplication([])
    cyclo_app.aboutToQuit.connect(on_about_to_quit)

    app_window = AppWindow()
    launch_window = StartupWindow(app_window)

    app_controller = AppController(app_window, launch_window)

    sys.exit(cyclo_app.exec())

if __name__ == "__main__":

    main()
