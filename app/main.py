import sys

import Utility.path_config

from PyQt6.QtWidgets import QApplication

from AppWindow import AppWindow
from AppController import AppController

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
        'LB': [80, 'mm'],               # Wsp. podpory nieprzesuwnej - B
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
        'F1': [None, 'N'],              # Siła na kole obiegowym 1
        'F2': [None, 'N'],              # Siła na kole obiegowym 2
        # Obliczone i dobrane średnice
        'dsc': [None, 'mm'],            # Średnica wału wejściowego - obliczona
        'dec': [None, 'mm'],            # Średnica mimośrodu - obliczona
        'dA': [None, 'mm'],             # Średnica pod podporę A
        'dB': [None, 'mm'],             # Średnica pod podporę B
        'de': [None, 'mm'],             # Średnica pod tarcze
        # Dobrany materiał i parametry
        'Materiał' : [None],            # Materiał wału
        'xz': [1, ''],                  # Współczynnik bezpieczeństwa
        'qdop': [0.00436, 'rad/m'],     # Dopuszczalny jednostkowy kąt skręcenia wału
        'tetadop': [0.001, 'rad'],      # Dopuszczalny kąt ugięcia wału
        'fdop': [0.030, 'mm'],          # Dopuszczalna strzałka ugięcia wału
        ## Łożyska podpora A
        # Dobór łożysk
        'Łożyska_podpora_A': [None],    # Łożyska
        'LhA': [20000, 'h'],            # Trwałość godzinowa
        'LrA': [None, 'obr'],           # Trwałość
        'CA': [None, 'kN'],             # Nośność
        'fdA': [1.80, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
        'ftA': [1.00, ''],              # Współczynnik zależny od temperatury pracy łożyska
        # Straty mocy
        'fA': [0.01, 'mm'],             # Współczynnik tarcia tocznego
        'dwAc': [None, 'mm'],           # Średnica elementu tocznego ł. podporowych - obliczona
        'Toczne_podpora_A': [None],     # Element toczny
        'SA': [None, 'mm'],             # Grubość pierścienia
        'NA': [None, 'W'],              # Starty mocy
        ## Łożyska podpora B
        # Dobór łożysk
        'Łożyska_podpora_B': [None],    # Łożyska
        'LhB': [20000, 'h'],            # Trwałość godzinowa
        'LrB': [None, 'obr'],           # Trwałość
        'CB': [None, 'kN'],             # Nośność
        'fdB': [1.60, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
        'ftB': [1.00, ''],              # Współczynnik zależny od temperatury pracy łożyska
        # Straty mocy
        'fB': [0.01, 'mm'],             # Współczynnik tarcia tocznego
        'dwBc': [None, 'mm'],           # Średnica elementu tocznego ł. podporowych - obliczona
        'Toczne_podpora_B': [None],     # Element toczny
        'SB': [None, 'mm'],             # Grubość pierścienia
        'NB': [None, 'W'],              # Starty mocy
        ## Łożyska centralne
        # Dobór łożysk
        'Łożyska_centralne': [None],    # Łożyska
        'Lhc': [20000, 'h'],            # Trwałość godzinowa
        'Ltc': [None, 'obr'],           # Trwałość
        'Cc': [None, 'kN'],             # Nośność
        'fdc': [1.00, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
        'ftc': [1.00, ''],              # Współczynnik zależny od temperatury pracy łożyska
        # Straty mocy
        'fc': [0.01, 'mm'],             # Współczynnik tarcia tocznego
        'rw1': [99, 'mm'],              # Promień koła toczengo (koło obiegowe)
        'dwcc': [None, 'mm'],           # Średnica elementu tocznego
        'Toczne_centralnych': [None],   # Element toczny
        'Sc': [None, 'mm'],             # Grubość pierścienia
        'Nc': [None, 'W'],              # Starty mocy
        }

    app_window = AppWindow()

    app_controller = AppController(data, app_window)
    app_window.show()

    sys.exit(cyclo_app.exec())

if __name__ == "__main__":

    main()
