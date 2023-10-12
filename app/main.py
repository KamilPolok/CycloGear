import sys

from PyQt6.QtWidgets import QApplication

from controller.DBController import DBController
from model.DatabaseHandler import DatabaseHandler
from view.Window import Window

def main():
    dbApp = QApplication([])
    dbHandler = DatabaseHandler()
    
    window = Window()
    window.show()

    displayController = DBController(model=dbHandler, view=window)

    sys.exit(dbApp.exec())

if __name__ == "__main__":
    main()
