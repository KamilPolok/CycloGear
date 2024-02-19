import math
import numpy as np

from DbHandler.controller.DBController import ViewSelectItemController
from DbHandler.model.DatabaseHandler import DatabaseHandler
from DbHandler.view.Window import Window

class InputShaftCalculator():
    def __init__(self):
        self.data = {
            # Napęd
            'nwe':[750, 'obr/min'],         # Prędkość obrotowa wejściowa
            'w0':[78,54, 'rad/s'],          # Prędkość kątowa wejściowa
            'Mwe': [26.67, 'Nm'],           # Moment wejściowy - moment skręcający
            # Zadane wymiary wału
            'L': [None, 'mm'],              # Całkowita długość wału wejściowego
            'LA': [None, 'mm'],             # Wsp. podpory przesuwnej - A
            'LB': [None, 'mm'],             # Wsp. podpory nieprzesuwnej - B
            'n': [2, ''],                   # Liczba kół obiegowych
            'L1': [None, 'mm'],             # Wsp. koła obiegowego 1
            'L2': [None, 'mm'],             # Wsp. koła obiegowego 2
            'e': [3, 'mm'],                 # Mimośród
            'B': [17, 'mm'],                # Długość koła obiegowego
            'x': [5, 'mm'],                 # Odległość pomiędzy dwoma kołami obiegowymi
            # Siły pochodzące od kół obiegowych
            'Fwzx': [4444.44, 'N'],         # Wypadkowa siła międzyzębna działająca w osi x
            'Fwzy': [2799.16, 'N'],         # Wypadkowa siła międzyzębn działająca w osi y
            'Fwm': [5602.25, 'N'],          # Wypadkowa siła w mechanizmie wyjściowym
            # Reakcje podporowe i siły działające na wał
            'Ra':[None, 'N'],               # Reakcja w podporze nieruchomej
            'Rb':[None, 'N'],               # Reakcja w podporze ruchomej
            'F': [None, 'N'],               # Siła pochodząca od koła obiegowego
            'F1': [None, 'N'],              # Siła na kole obiegowym 1
            'F2': [None, 'N'],              # Siła na kole obiegowym 2
            # Obliczone i dobrane średnice
            'dsc': [None, 'mm'],            # Średnica wału wejściowego - obliczona
            'dec': [None, 'mm'],            # Średnica mimośrodu - obliczona
            'dA': [None, 'mm'],             # Średnica pod podporę A
            'dB': [None, 'mm'],             # Średnica pod podporę B
            'de': [None, 'mm'],             # Średnica pod tarcze
            # Dobrany materiał i parametry
            'Materiał' : None,              # Materiał wału
            'xz': [None, ''],               # Współczynnik bezpieczeństwa
            'qdop': [None, 'rad/m'],        # Dopuszczalny jednostkowy kąt skręcenia wału
            'tetadop': [None, 'rad'],       # Dopuszczalny kąt ugięcia wału
            'fdop': [None, 'mm'],           # Dopuszczalna strzałka ugięcia wału
            ## Łożyska podpora A
            # Dobór łożysk
            'Łożyska_podpora_A': None,      # Łożyska
            'LhA': [None, 'h'],             # Trwałość godzinowa
            'LrA': [None, 'obr'],           # Trwałość
            'CA': [None, 'kN'],             # Nośność
            'fdA': [None, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
            'ftA': [None, ''],              # Współczynnik zależny od temperatury pracy łożyska
            # Straty mocy
            'fA': [None, 'mm'],             # Współczynnik tarcia tocznego
            'dwAc': [None, 'mm'],           # Średnica elementu tocznego ł. podporowych - obliczona
            'Toczne_podpora_A': None,       # Element toczny
            'SA': [None, 'mm'],             # Grubość pierścienia
            'NA': [None, 'W'],              # Starty mocy
            ## Łożyska podpora B
            # Dobór łożysk
            'Łożyska_podpora_B': None,      # Łożyska
            'LhB': [None, 'h'],             # Trwałość godzinowa
            'LrB': [None, 'obr'],           # Trwałość
            'CB': [None, 'kN'],             # Nośność
            'fdB': [None, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
            'ftB': [None, ''],              # Współczynnik zależny od temperatury pracy łożyska
            # Straty mocy
            'fB': [None, 'mm'],             # Współczynnik tarcia tocznego
            'dwBc': [None, 'mm'],           # Średnica elementu tocznego ł. podporowych - obliczona
            'Toczne_podpora_B': None,       # Element toczny
            'SB': [None, 'mm'],             # Grubość pierścienia
            'NB': [None, 'W'],              # Starty mocy
            ## Łożyska centralne
            # Dobór łożysk
            'Łożyska_centralne': None,      # Łożyska
            'Lhc': [None, 'h'],             # Trwałość godzinowa
            'Ltc': [None, 'obr'],           # Trwałość
            'Cc': [None, 'kN'],             # Nośność
            'fdc': [None, ''],              # Współczynnik zależny od zmiennych obciążeń dynamicznych
            'ftc': [None, ''],              # Współczynnik zależny od temperatury pracy łożyska
            # Straty mocy
            'fc': [None, 'mm'],             # Współczynnik tarcia tocznego
            'rw1': [99, 'mm'],              # Promień koła toczengo (koło obiegowe)
            'dwcc': [None, 'mm'],           # Średnica elementu tocznego
            'Toczne_centralnych': None,     # Element toczny
            'Sc': [None, 'mm'],             # Grubość pierścienia
            'Nc': [None, 'W'],              # Starty mocy
        }

    def calculate_preliminary_attributes(self):
        fwzx = self.data['Fwzx'][0]
        fwzy = self.data['Fwzy'][0]
        fwm = self.data['Fwm'][0]

        self.data['F'][0] = (fwzx**2 + (fwm - fwzy)**2)**0.5
        
    def calculate_bearings_attributes(self):
        """
        Calculate attributes of support and central bearings.
        """
        # Calculate support A bearing attributes
        Dw = self.data['Łożyska_podpora_A']['Dw'][0]
        Dz = self.data['Łożyska_podpora_A']['Dz'][0]

        dw = 0.25 * (Dz - Dw)

        self.data['dwAc'][0] = dw

        # Calculate support B bearing attributes
        Dw = self.data['Łożyska_podpora_B']['Dw'][0]
        Dz = self.data['Łożyska_podpora_B']['Dz'][0]

        dw = 0.25 * (Dz - Dw)

        self.data['dwBc'][0] = dw

        # Calculate central bearings attributes
        Dw = self.data['Łożyska_centralne']['Dw'][0]
        Dz = self.data['Łożyska_centralne']['E'][0]

        dw = 0.25 * (Dz - Dw)

        self.data['dwcc'][0] = dw
    
    def calculate_support_A_bearing_load_capacity(self):
        """
        Calculate load capacity of the support A bearing.
        """
        nwe = self.data['nwe'][0]
        lh = self.data['LhA'][0]
        fd = self.data['fdA'][0]
        ft = self.data['ftA'][0]
        p = 3.0

        ra = self.data['Ra'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = ra * np.power(l, 1 / p) * ft / fd / 1000 # [kN]

        self.data['LrA'][0] = l
        self.data['CA'][0] = c

    def calculate_support_B_bearing_load_capacity(self):
        """
        Calculate load capacity of the support B bearing.
        """
        nwe = self.data['nwe'][0]
        lh = self.data['LhB'][0]
        fd = self.data['fdB'][0]
        ft = self.data['ftB'][0]
        p = 3.0

        ra = self.data['Ra'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = ra * np.power(l, 1 / p) * ft / fd / 1000 # [kN]

        self.data['LrB'][0] = l
        self.data['CB'][0] = c

    def calculate_central_bearing_load_capacity(self):
        """
        Calculate load capacity of central bearing.
        """
        nwe = self.data['nwe'][0]
        lh = self.data['Lhc'][0]
        fd = self.data['fdc'][0]
        ft = self.data['ftc'][0]
        p = 3.0

        f = self.data['F'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = f * np.power(l, 1 / p) * ft / fd/ 1000 # [kN]

        self.data['Ltc'][0] = l
        self.data['Cc'][0] = c

    def calculate_bearings_power_loss(self):
        """
        Calculate power loss in bearin.
        """
        w0 = self.data['w0'][0]
        e = self.data['e'][0]
        fA = self.data['fA'][0]
        fc = self.data['fc'][0]
        rw1 = self.data['rw1'][0]
        Ra = self.data['Ra'][0]
        Rb = self.data['Rb'][0]
        F = self.data['F'][0]

        # Calculate power loss for support A bearing
        dw = self.data['Toczne_podpora_A']['D'][0]
        Dw = self.data['Łożyska_podpora_A']['Dw'][0]

        S = dw / 2
        NA = fA * 0.001 * w0 * (1 + (Dw + 2 * S) / dw) * (1 + e / rw1) * 4 * np.abs(Ra) / np.pi

        self.data['SA'][0] = S
        self.data['NA'][0] = NA

        # Calculate power loss for support B bearing
        dw = self.data['Toczne_podpora_B']['D'][0]
        Dw = self.data['Łożyska_podpora_B']['Dw'][0]

        S = dw / 2
        NB = fA * 0.001 * w0 * (1 + (Dw + 2 * S) / dw) * (1 + e / rw1) * 4 * np.abs(Rb) / np.pi

        self.data['SB'][0] = S
        self.data['NB'][0] = NB

        # Calculate power loss for central bearings
        dw = self.data['Toczne_centralnych']['D'][0]
        Dw = self.data['Łożyska_centralne']['Dw'][0]
        Dz = self.data['Łożyska_centralne']['Dz'][0]

        S = 0.15 * (Dz - Dw)
        Nc = fc * 0.001 * w0 * (1 + (Dw + 2 * S) / dw) * (1 + e / rw1) * 4 * F / np.pi

        self.data['Sc'][0] = S
        self.data['Nc'][0] = Nc
         
    def open_shaft_material_selection(self, callback):
        """
        Open the window for selection of the shaft material

        Args:
            callback (function): A callback function that will be called with the selected item's data as its argument.
        """
        db_handler = DatabaseHandler()
        subwindow = Window()
        subwindow.setWindowTitle("Dobór materiału")
        tables_group_name = 'wał wejściowy-materiały'
        available_tables = db_handler.getAvailableTables(tables_group_name)
        limits = db_handler.getTableItemsFilters(tables_group_name)
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(callback)
        subwindow.exec()

    def open_support_A_bearing_selection(self, callback):
        """
        Open the window for selection of the support A bearing.

        Args:
            callback (function): A callback function that will be called with the selected item's data as its argument.
        """

        # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór łożyska")
        # Specify the group name of the tables you want to take for consideration
        tables_group_name = 'wał wejściowy-łożyska-podporowe'
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['Dw']['min'] = self.data['dA'][0]
        limits['C']['min'] = self.data['CA'][0]
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(callback)
        subwindow.exec()

    def open_support_B_bearing_selection(self, callback):
        """
        Open the window for selection of the support B bearing.

        Args:
            callback (function): A callback function that will be called with the selected item's data as its argument.
        """
        # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór łożyska")
        # Specify the group name of the tables you want to take for consideration
        tables_group_name = 'wał wejściowy-łożyska-podporowe'
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['Dw']['min'] = self.data['dB'][0]
        limits['C']['min'] = self.data['CB'][0]
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(callback)
        subwindow.exec()

    def open_central_bearing_selection(self, callback):
        """
        Open the window for selection of the central bearing.

        Args:
            callback (function): A callback function that will be called with the selected item's data as its argument.
        """
        # # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór łożyska")
        # Specify the group name of the tables you want to take for consideration
        tables_group_name = 'wał wejściowy-łożyska-centralne'
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['Dw']['min'] = self.data['de'][0]
        limits['C']['min'] = self.data['Cc'][0]
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(callback)
        subwindow.exec()

    def open_support_A_bearing_rolling_element_selection(self, callback):
        """
        Open the window for selection of support A bearing rolling element.

        Args:
            callback (function): A callback function that will be called with the selected item's data as its argument.
        """
        # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór elementu tocznego")
        # Specify the group name of the tables you want to take for consideration
        tables_group_name = f"wał wejściowy-elementy toczne-{self.data['Łożyska_podpora_A']['elementy toczne'][0]}"
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['D']['min'] = math.floor(self.data['dwAc'][0]) - 1
        limits['D']['max'] = math.ceil(self.data['dwAc'][0]) + 1
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(callback)
        subwindow.exec()

    def open_support_B_bearing_rolling_element_selection(self, callback):
        """
        Open the window for selection of support A bearing rolling element.

        Args:
            callback (function): A callback function that will be called with the selected item's data as its argument.
        """
        # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór elementu tocznego")
        # Specify the group name of the tables you want to take for consideration
        tables_group_name = f"wał wejściowy-elementy toczne-{self.data['Łożyska_podpora_B']['elementy toczne'][0]}"
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['D']['min'] = math.floor(self.data['dwBc'][0]) - 1
        limits['D']['max'] = math.ceil(self.data['dwBc'][0]) + 1
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(callback)
        subwindow.exec()

    def open_central_bearing_rolling_element_selection(self, callback):
        """
        Open the window for selection of central bearing rolling element.

         Args:
            callback (function): A callback function that will be called with the selected item's data as its argument.
        """
        # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór elementu tocznego")
        # Specify the group name of the tables you want to take for consideration
        tables_group_name = f"wał wejściowy-elementy toczne-{self.data['Łożyska_centralne']['elementy toczne'][0]}"
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['D']['min'] = math.floor(self.data['dwcc'][0]) - 1
        limits['D']['max'] = math.ceil(self.data['dwcc'][0]) + 1
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(callback)
        subwindow.exec()

    def get_data(self):
        """
        Get component data.
        """
        return self.data
    
    def set_data(self, data):
        """
        Set component data.
        """
        self.data.update(data)
    
    def update_data(self, data):
        """
        Update component data.

        :param data: New data to update with the component data.
        """
        for key, value in data.items():
            if key in self.data:
                self.data[key] = value
