import math
import numpy as np

from DbHandler.controller.DBController import ViewSelectItemController
from DbHandler.model.DatabaseHandler import DatabaseHandler
from DbHandler.view.Window import Window

from ..common.common_functions import fetch_data_subset

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
            'rw1': [99, 'mm'],              # Promień koła toczengo (koło obiegowe)
            # Dobrany materiał i parametry
            'Materiał' : None,              # Materiał wału
            'xz': [None, ''],               # Współczynnik bezpieczeństwa
            'qdop': [None, 'rad/m'],        # Dopuszczalny jednostkowy kąt skręcenia wału
            'tetadop': [None, 'rad'],       # Dopuszczalny kąt ugięcia wału
            'fdop': [None, 'mm'],           # Dopuszczalna strzałka ugięcia wału
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
            # Obliczone wymiary wału
            'dsc': [None, 'mm'],            # Średnica wału wejściowego - obliczona
            'dec': [None, 'mm'],            # Średnica mimośrodu - obliczona
            # Łożyska
            'Bearings': {
              # Podpora A
              'support_A': {                         
                'data': None,               # Parametry łożyska
                'rolling_elements': None,   # Elementy toczne
                'dip': [None, 'mm'],        # Średnica wewnętrzna łożyska - na podstawie zaprojektowanego wału
                'di': [None, 'mm'],         # Średnica wewnętrzna łożyska
                'do': [None, 'mm'],         # Średnica zewnętrzna łożyska
                'drc': [None, 'mm'],        # Średnica elementów tocznych - obliczona
                'Lh': [None, 'h'],          # Trwałość godzinowa
                'Lr': [None, 'obr'],        # Trwałość
                'C': [None, 'kN'],          # Nośność
                'fd': [None, ''],           # Współczynnik zależny od zmiennych obciążeń dynamicznych
                'ft': [None, ''],           # Współczynnik zależny od temperatury pracy łożyska
                'f': [None, 'mm'],          # Współczynnik tarcia tocznego
                'S': [None, 'mm'],          # Grubość pierścienia
                'N': [None, 'W'],           # Starty mocy           
              },
               # Podpora B
              'support_B': {                         
                'data': None,               # Parametry łożyska
                'rolling_elements': None,   # Elementy toczne
                'dip': [None, 'mm'],       # Średnica wewnętrzna łożyska - na podstawie zaprojektowanego wału
                'di': [None, 'mm'],         # Średnica wewnętrzna łożyska
                'do': [None, 'mm'],         # Średnica zewnętrzna łożyska
                'drc': [None, 'mm'],        # Średnica elementów tocznych - obliczona
                'Lh': [None, 'h'],          # Trwałość godzinowa
                'Lr': [None, 'obr'],        # Trwałość
                'C': [None, 'kN'],          # Nośność
                'fd': [None, ''],           # Współczynnik zależny od zmiennych obciążeń dynamicznych
                'ft': [None, ''],           # Współczynnik zależny od temperatury pracy łożyska
                'f': [None, 'mm'],          # Współczynnik tarcia tocznego
                'S': [None, 'mm'],          # Grubość pierścienia
                'N': [None, 'W'],           # Starty mocy           
              },
               # Wykorbienia pod koła cykloidalne
              'eccentrics': {                         
                'data': None,               # Parametry łożyska
                'rolling_elements': None,   # Elementy toczne
                'di': [None, 'mm'],         # Średnica wewnętrzna łożyska
                'do': [None, 'mm'],         # Średnica zewnętrzna łożyska
                'dip': [None, 'mm'],       # Średnica wewnętrzna łożyska - na podstawie zaprojektowanego wału
                'drc': [None, 'mm'],        # Średnica elementów tocznych - obliczona
                'Lh': [None, 'h'],          # Trwałość godzinowa
                'Lr': [None, 'obr'],        # Trwałość
                'C': [None, 'kN'],          # Nośność
                'fd': [None, ''],           # Współczynnik zależny od zmiennych obciążeń dynamicznych
                'ft': [None, ''],           # Współczynnik zależny od temperatury pracy łożyska
                'f': [None, 'mm'],          # Współczynnik tarcia tocznego
                'S': [None, 'mm'],          # Grubość pierścienia
                'N': [None, 'W'],           # Starty mocy           
              }
            }
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
        Dw = self.data['Bearings']['support_A']['data']['Dw'][0]
        Dz = self.data['Bearings']['support_A']['data']['Dz'][0]

        dw = 0.25 * (Dz - Dw)

        self.data['Bearings']['support_A']['drc'][0] = dw
        self.data['Bearings']['support_A']['di'][0] = Dw
        self.data['Bearings']['support_A']['do'][0] = Dz

        # Calculate support B bearing attributes
        Dw = self.data['Bearings']['support_B']['data']['Dw'][0]
        Dz = self.data['Bearings']['support_B']['data']['Dz'][0]

        dw = 0.25 * (Dz - Dw)

        self.data['Bearings']['support_B']['drc'][0] = dw
        self.data['Bearings']['support_B']['di'][0] = Dw
        self.data['Bearings']['support_B']['do'][0] = Dz

        # Calculate central bearings attributes
        Dw = self.data['Bearings']['eccentrics']['data']['Dw'][0]
        Dz = self.data['Bearings']['eccentrics']['data']['E'][0]

        dw = 0.25 * (Dz - Dw)

        self.data['Bearings']['eccentrics']['drc'][0] = dw
        self.data['Bearings']['eccentrics']['di'][0] = Dw
        self.data['Bearings']['eccentrics']['do'][0] = Dz
    
    def calculate_support_A_bearing_load_capacity(self):
        """
        Calculate load capacity of the support A bearing.
        """
        nwe = self.data['nwe'][0]
        lh = self.data['Bearings']['support_A']['Lh'][0]
        fd = self.data['Bearings']['support_A']['fd'][0]
        ft = self.data['Bearings']['support_A']['ft'][0]
        p = 3.0

        ra = self.data['Ra'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = ra * np.power(l, 1 / p) * ft / fd / 1000 # [kN]

        self.data['Bearings']['support_A']['Lr'][0] = l
        self.data['Bearings']['support_A']['C'][0] = c

    def calculate_support_B_bearing_load_capacity(self):
        """
        Calculate load capacity of the support B bearing.
        """
        nwe = self.data['nwe'][0]
        lh = self.data['Bearings']['support_B']['Lh'][0]
        fd = self.data['Bearings']['support_B']['fd'][0]
        ft = self.data['Bearings']['support_B']['ft'][0]
        p = 3.0

        ra = self.data['Ra'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = ra * np.power(l, 1 / p) * ft / fd / 1000 # [kN]

        self.data['Bearings']['support_B']['Lr'][0] = l
        self.data['Bearings']['support_B']['C'][0] = c

    def calculate_central_bearing_load_capacity(self):
        """
        Calculate load capacity of central bearing.
        """
        nwe = self.data['nwe'][0]
        lh = self.data['Bearings']['eccentrics']['Lh'][0]
        fd = self.data['Bearings']['eccentrics']['fd'][0]
        ft = self.data['Bearings']['eccentrics']['ft'][0]

        p = 3.0

        f = self.data['F'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = f * np.power(l, 1 / p) * ft / fd/ 1000 # [kN]

        self.data['Bearings']['eccentrics']['Lr'][0] = l
        self.data['Bearings']['eccentrics']['C'][0] = c

    def calculate_bearings_power_loss(self):
        """
        Calculate power loss in bearin.
        """
        w0 = self.data['w0'][0]
        e = self.data['e'][0]
        rw1 = self.data['rw1'][0]

        # Calculate power loss for support A bearing
        dw = self.data['Bearings']['support_A']['rolling_elements']['D'][0]
        Dw = self.data['Bearings']['support_A']['data']['Dw'][0]
        f = self.data['Bearings']['support_A']['f'][0]
        Ra = self.data['Ra'][0]

        S = dw / 2
        N = f * 0.001 * w0 * (1 + (Dw + 2 * S) / dw) * (1 + e / rw1) * 4 * np.abs(Ra) / np.pi

        self.data['Bearings']['support_A']['S'][0] = S
        self.data['Bearings']['support_A']['N'][0] = N

        # Calculate power loss for support B bearing
        dw = self.data['Bearings']['support_B']['rolling_elements']['D'][0]
        Dw = self.data['Bearings']['support_B']['data']['Dw'][0]
        f = self.data['Bearings']['support_B']['f'][0]
        Rb = self.data['Rb'][0]

        S = dw / 2
        N = f * 0.001 * w0 * (1 + (Dw + 2 * S) / dw) * (1 + e / rw1) * 4 * np.abs(Rb) / np.pi

        self.data['Bearings']['support_B']['S'][0] = S
        self.data['Bearings']['support_B']['N'][0] = N

        # Calculate power loss for central bearings
        dw = self.data['Bearings']['eccentrics']['rolling_elements']['D'][0]
        Dw = self.data['Bearings']['eccentrics']['data']['Dw'][0]
        Dz = self.data['Bearings']['eccentrics']['data']['Dz'][0]
        f = self.data['Bearings']['eccentrics']['f'][0]
        F = self.data['F'][0]

        S = 0.15 * (Dz - Dw)
        N = f * 0.001 * w0 * (1 + (Dw + 2 * S) / dw) * (1 + e / rw1) * 4 * F / np.pi

        self.data['Bearings']['eccentrics']['S'][0] = S
        self.data['Bearings']['eccentrics']['N'][0] = N

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
        limits['Dw']['min'] = self.data['Bearings']['support_A']['dip'][0]
        limits['C']['min'] = self.data['Bearings']['support_A']['C'][0]
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
        limits['Dw']['min'] = self.data['Bearings']['support_B']['dip'][0]
        limits['C']['min'] = self.data['Bearings']['support_B']['dip'][0]
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
        limits['Dw']['min'] = self.data['Bearings']['eccentrics']['dip'][0]
        limits['C']['min'] = self.data['Bearings']['eccentrics']['dip'][0]
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
        tables_group_name = f"wał wejściowy-elementy toczne-{self.data['Bearings']['support_A']['data']['elementy toczne'][0]}"
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['D']['min'] = math.floor(self.data['Bearings']['support_A']['drc'][0]) - 1
        limits['D']['max'] = math.ceil(self.data['Bearings']['support_A']['drc'][0]) + 1
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
        tables_group_name = f"wał wejściowy-elementy toczne-{self.data['Bearings']['support_B']['data']['elementy toczne'][0]}"
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['D']['min'] = math.floor(self.data['Bearings']['support_B']['drc'][0]) - 1
        limits['D']['max'] = math.ceil(self.data['Bearings']['support_B']['drc'][0]) + 1
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
        tables_group_name = f"wał wejściowy-elementy toczne-{self.data['Bearings']['eccentrics']['data']['elementy toczne'][0]}"
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['D']['min'] = math.floor(self.data['Bearings']['eccentrics']['drc'][0]) - 1
        limits['D']['max'] = math.ceil(self.data['Bearings']['eccentrics']['drc'][0]) + 1
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

        Args (dict): New data to update the component data with.
        """   
        fetch_data_subset(self.data, data)
