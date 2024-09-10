import path_config

import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QCoreApplication

from main_interface.view.MainWindow import MainWindow
from main_interface.controller.main_controller import MainController

def on_about_to_quit():
    # Perform necessary checks or operations
    QCoreApplication.processEvents()

def main():
    cyclo_app = QApplication([])
    cyclo_app.aboutToQuit.connect(on_about_to_quit)

    main_window = MainWindow()

    main_controller = MainController(main_window)

    sys.exit(cyclo_app.exec_())

if __name__ == "__main__":

    main()
