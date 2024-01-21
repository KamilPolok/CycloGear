import sys
import os

root_directory = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.append(root_directory)

from PyQt6.QtWidgets import QApplication

from AppWindow import AppWindow
from app.AppController import AppController

def main():
    cyclo_app = QApplication([])

    data = {
        # Napęd
        'nwe':[750, 'obr/min'],         # Prędkość obrotowa wejściowa
        'w0':[78,54, 'rad/s'],          # Prędkość kątowa wejściowa
        'Mwe': [26.67, 'Nm'],           # Moment wejściowy - moment skręcający
        # Zadane wymiary wału
        'L': [100, 'mm'],               # Całkowita długość wału wejściowego
        'LA': [15, 'mm'],               # Wsp. podpory przesuwnej - A
        'LB': [52, 'mm'],               # Wsp. podpory nieprzesuwnej - B
        'n': [2, ''],                    # Liczba kół obiegowych
        'L1': [24, 'mm'],               # Wsp. koła obiegowego 1
        'L2': [None, 'mm'],             # Wsp. koła obiegowego 2
        'e': [3, 'mm'],                 # Mimośród
        'B': [17, 'mm'],                # Długość koła obiegowego
        'x': [5, 'mm'],                 # Odległość pomiędzy dwoma kołami obiegowymi
        # Reakcje podporowe i siły działające na wał
        'Ra':[None, 'N'],               # Reakcja w podporze nieruchomej
        'Rb':[None, 'N'],               # Reakcja w podporze ruchomej
        'F': [5254.56, 'N'],            # Siła pochodząca od koła obiegowego
        # Obliczone i dobrane średnice
        'dsc': [None, 'mm'],            # Średnica wału wejściowego - obliczona
        'ds': [None, 'mm'],             # Średnica wału wejściowego - dostosowana do łożyska
        'dec': [None, 'mm'],            # Średnica mimośrodu - obliczona
        'de': [None, 'mm'],             # Średnica mimośrodu - dostosowana do łożyska
        # Dobrany materiał i parametry
        'Materiał' : [None],            # Materiał wału
        'xz': [1, ''],                  # Współczynnik bezpieczeństwa
        'qdop': [0.00436, 'rad/m'],     # Dopuszczalny jednostkowy kąt skręcenia wału
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
        'f': [0.01, 'mm'],              # Luz w łożysku - nie jestem pewien
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

    app_window = AppWindow()

    app_controller = AppController(data, app_window)
    app_window.show()

    sys.exit(cyclo_app.exec())

if __name__ == "__main__":
    main()
