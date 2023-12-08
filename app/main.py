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
        # Napęd
        'nwe':[750, 'obr/min'],         # Prędkość obrotowa wejściowa
        'w0':[78,54, 'rad/s'],          # Prędkość kątowa wejściowa
        'Mwe': [26.67, 'Nm'],           # Moment wejściowy
        # Zadane wymiary wału
        'L': [80, 'mm'],                # Długość wału
        'LA': [38, 'mm'],               # Wsp podpory nieruchomej A
        'LB': [75, 'mm'],               # Wsp podpory ruchomej B
        'L1': [47, 'mm'],               # Wsp koła obiegowego 1
        'L2': [64, 'mm'],               # Wsp koła obiegowego 2
        'e': [10, 'mm'],                # Mimośród
        # Reakcje podporowe i siły działające na wał
        'Ra':[None, 'N'],               # Reakcja w podporze nieruchomej
        'Rb':[None, 'N'],               # Reakcja w podporze ruchomej
        'F': [5254.56, 'N'],           # Siła pochodząca od koła obiegowego
        # Obliczone i dobrane średnice
        'dsc': [None, 'mm'],            # Średnica wału wejściowego - obliczona
        'ds': [None, 'mm'],             # Średnica wału wejściowego - dostosowana do łożyska
        'dec': [None, 'mm'],            # Średnica mimośrodu - obliczona
        'de': [None, 'mm'],             # Średnica mimośrodu - dostosowana do łożyska
        # Dobrany materiał
        'Materiał' : [None],            # Materiał wału
        'xz': [1, ''],                  # Współczynnik bezpieczeństwa
        # Łożyska podporow
        'Łożyska_podporowe': [None],    # Łożyska podporowe
        'Lhp': [20000, 'h'],            # Trwałość godzinowa ł. podporowych
        'Lrp': [None, 'obr'],           # Trwałość ł. podporowych
        'Cr': [None, 'kN'],             # Nośność ł. podporowych - obliczona
        # Dodaj                         # Nośność ł. podporowych - dostosowana do łożyska
        'fdp': [1.80, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
        'ftp': [1.00, ''],              # Współczynnik zależny od temperatury pracy łożyska
        # Łożyska centralne
        'Łożyska_centralne': [None],    # Łożyska centralne
        'Lhc': [20000, 'h'],            # Trwałość godzinowa ł. centralnych
        'Ltc': [None, 'obr'],           # Trwałość ł. centralnych
        'Cc': [None, 'kN'],             # Nośność ł. centralnych - obliczona
        # Dodaj                         # Nośność ł. centralnych - dostosowana do łożyska
        'fdc': [1.00, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
        'ftc': [1.00, ''],              # Współczynnik zależny od temperatury pracy łożyska
        # Straty mocy
        'f': [0.01, 'mm'],               # Luz w łożysku - nie jestem pewien
        'rw1': [99, 'mm'],              # Promień koła toczengo (koło obiegowe)
        'dwpc': [None, 'mm'],           # Średnica elementu tocznego ł. podporowych - obliczona
        'Toczne_podporowych': [None],   # Element toczny ł. podporowych
        'Sp': [None, 'mm'],             # Grubość pierścienia ł. podporowych
        'Np': [None, 'W'],              # Starty mocy ł. podporowych
        'dwcc': [None, 'mm'],           # Średnica elementu tocznego ł. centralnych - obliczona
        'Toczne_centralnych': [None],   # Element toczny ł. centralnych
        'Sc': [None, 'mm'],             # Grubość pierścienia ł. centralnych
        'Nc': [None, 'W'],              # Starty mocy ł. centralnych
        }

    main_window = MainWindow()

    main_window_controller = MainWindowController(data, main_window)
    main_window.show()

    sys.exit(cyclo_app.exec())

if __name__ == "__main__":
    main()
