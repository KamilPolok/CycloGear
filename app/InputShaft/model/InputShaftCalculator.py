import math
import numpy as np
from functools import partial

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
                'F': None,                  # Siła działająca na łożysko 
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
                'F': None,                  # Siła działająca na łożysko
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
               # Wykorbienia pod koła cykloidalne
              'eccentrics': {                         
                'data': None,               # Parametry łożyska
                'rolling_elements': None,   # Elementy toczne
                'F': None,                  # Siła działająca na łożysko
                'l': None,                  # Położenie łożyska na wale
                'di': [None, 'mm'],         # Średnica wewnętrzna łożyska
                'do': [None, 'mm'],         # Średnica zewnętrzna łożyska
                'dip': [None, 'mm'],        # Średnica wewnętrzna łożyska - na podstawie zaprojektowanego wału
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
        self._add_data_reference()

    def _add_data_reference(self):
        self.data['Bearings']['support_A']['F'] = self.data['Ra']
        self.data['Bearings']['support_B']['F'] = self.data['Rb']
        self.data['Bearings']['eccentrics']['F'] = self.data['F']

        self.data['Bearings']['support_A']['l'] = self.data['LA']
        self.data['Bearings']['support_B']['l'] = self.data['LB']
        self.data['Bearings']['eccentrics']['l'] = self.data['L1']

    def calculate_preliminary_attributes(self):
        fwzx = self.data['Fwzx'][0]
        fwzy = self.data['Fwzy'][0]
        fwm = self.data['Fwm'][0]

        self.data['F'][0] = (fwzx**2 + (fwm - fwzy)**2)**0.5
        
    def calculate_bearings_attributes(self):
        """
        Calculate bearings attributes.
        """
        for bearing_section_id, attributes in self.data['Bearings'].items():
            Dz = attributes['data']['E'][0] if bearing_section_id == 'eccentrics' else attributes['data']['Dz'][0]
            Dw = attributes['data']['Dw'][0]

            dw = 0.25 * (Dz - Dw)

            attributes['drc'][0] = dw
            attributes['di'][0] = Dw
            attributes['do'][0] = Dz
    
    def calculate_bearing_load_capacity(self, bearing_section_id):
        """
        Calculate bearing load capacity.
        """
        p = 3.0
        nwe = self.data['nwe'][0]
        attributes = self.data['Bearings'][bearing_section_id]
    
        lh = attributes['Lh'][0]
        fd = attributes['fd'][0]
        ft = attributes['ft'][0]
        F = attributes['F'][0]

        l = 60 * lh * nwe / np.power(10, 6)
        c = np.abs(F) * np.power(l, 1 / p) * ft / fd / 1000 # [kN]

        attributes['Lr'][0] = l
        attributes['C'][0] = c

    def calculate_bearings_power_loss(self):
        """
        Calculate bearings power loss.
        """
        w0 = self.data['w0'][0]
        e = self.data['e'][0]
        rw1 = self.data['rw1'][0]
        for bearing_section_id, attributes in self.data['Bearings'].items():
            dw = attributes['rolling_elements']['D'][0]
            Dw = attributes['data']['Dw'][0]
            Dz = attributes['data']['Dz'][0]
            f = attributes['f'][0]
            F = attributes['F'][0]
            
            S = 0.15 * (Dz - Dw) if bearing_section_id == 'eccentrics' else dw / 2
            N = f * 0.001 * w0 * (1 + (Dw + 2 * S) / dw) * (1 + e / rw1) * 4 * np.abs(F) / np.pi

            attributes['S'][0] = S
            attributes['N'][0] = N

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

    def open_bearing_selection(self, bearing_section_id, callback):
        """
        Open the window for bearing selection the.

        Args:
            bearing_section_id (str): Id of section that specifies the bearing location.
            callback (function): Callback function that will be called with the selected item's data as its argument.
        """
        # Specify the name of the tables to open
        if bearing_section_id == 'support_A' or  bearing_section_id == 'support_B':
            tables_group_name = 'wał wejściowy-łożyska-podporowe'
        elif bearing_section_id == 'eccentrics':
            tables_group_name = 'wał wejściowy-łożyska-centralne'

        # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór łożyska")
        # Get available tables
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['Dw']['min'] = self.data['Bearings'][bearing_section_id]['dip'][0]
        limits['C']['min'] = self.data['Bearings'][bearing_section_id]['C'][0]
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(partial(callback, bearing_section_id))
        subwindow.exec()

    def open_rolling_element_selection(self, bearing_section_id, callback):
        """
        Open the window for rolling element selection.

        Args:
            bearing_section_id (str): Id of section that specifies the bearing location for which the rollin 
                                      elements are being selected.
            callback (function): Callback function that will be called with the selected item's data as its argument.
        """
        # Get acces to the database
        db_handler = DatabaseHandler()
        # Create a subwindow that views GUI for the DatabaseHandler
        subwindow = Window()
        subwindow.setWindowTitle("Dobór elementu tocznego")
        # Get available tables
        tables_group_name = f"wał wejściowy-elementy toczne-{self.data['Bearings'][bearing_section_id]['data']['elementy toczne'][0]}"
        available_tables = db_handler.getAvailableTables(tables_group_name)
        # Specify the limits for the group of tables
        limits = db_handler.getTableItemsFilters(tables_group_name)
        limits['D']['min'] = math.floor(self.data['Bearings'][bearing_section_id]['drc'][0]) - 1
        limits['D']['max'] = math.ceil(self.data['Bearings'][bearing_section_id]['drc'][0]) + 1
        # Setup the controller for the subwindow
        view_select_items_ctrl = ViewSelectItemController(db_handler, subwindow, available_tables, limits)
        subwindow.itemDataSignal.connect(partial(callback, bearing_section_id))
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
        fetch_data_subset(self.data, data)
    
    def update_data(self, data):
        """
        Update component data.

        Args (dict): New data to update the component data with.
        """   
        fetch_data_subset(self.data, data)
