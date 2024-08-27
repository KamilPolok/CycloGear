import sqlite3
import pandas as pd
import os
import sys


# Function to determine if we're running as a PyInstaller bundle
def is_frozen():
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# Function to get the correct base directory
def get_base_dir():
    if is_frozen():
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS.
        return sys._MEIPASS
    else:
        # If it's run in a normal Python environment, return the directory
        # containing this file.
        return os.path.dirname(os.path.abspath(__file__))

base_dir = get_base_dir()

config_path = os.path.join(base_dir, '..', '..', 'config.py')
config_dir = os.path.dirname(config_path)

# Add the config directory to sys.path if not already added
if config_dir not in sys.path:
    sys.path.append(config_dir)


from config import DATA_PATH, DATA_DIR_NAME, dependencies_path

database_tables = [
    {   
        "name": "wał czynny-łożyska-podporowe-kulkowe",
        "csvName": "wal_czynny-lozyska-podporowe-kulkowe.csv",
        "headers": ["Kod", "Dw [mm]", "Dz [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]", "elementy toczne"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'TEXT']
    },
    {
        "name": "wał czynny-łożyska-podporowe-walcowe",
        "csvName": "wal_czynny-lozyska-podporowe-walcowe.csv",
        "headers": ["Kod", "Dw [mm]", "Dz [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]", "elementy toczne"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'TEXT']
    },
    {
        "name": "wał czynny-łożyska-centralne-walcowe",
        "csvName": "wal_czynny-lozyska-centralne-walcowe.csv",
        "headers": ["Kod", "Dw [mm]", "Dz [mm]", "E [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]", "elementy toczne"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'REAL', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'TEXT']
    },
    {
        "name": "wał czynny-łożyska-centralne-igiełkowe",
        "csvName": "wal_czynny-lozyska-centralne-igielkowe.csv",
        "headers": ["Kod", "Dw [mm]", "Dz [mm]", "E [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]", "elementy toczne"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'REAL', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'TEXT']
    },
    {
        "name": "wał czynny-materiały",
        "csvName": "wal_czynny-materialy.csv",
        "headers": [ "Oznaczenie", "Rm [MPa]", "Re [MPa]", "Zgj [MPa]", "Zgo [MPa]", "Zsj [MPa]", "Zso [MPa]", "E [MPa]", "G [MPa]", "g [kg/m3]" ],
        "types": [ 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER' ]
    },
    {
        "name": "wał czynny-elementy toczne-kulki",
        "csvName": "wal_czynny-elementy_toczne-kulki.csv",
        "headers": [ "Kod", "D" ],
        "types": [ 'STRING', 'INTEGER']
    },
    {
        "name": "wał czynny-elementy toczne-wałeczki",
        "csvName": "wal_czynny-elementy_toczne-waleczki.csv",
        "headers": [ "Kod", "D" ],
        "types": [ 'STRING', 'INTEGER']
    },
    {
        "name": "wał czynny-elementy toczne-igiełki",
        "csvName": "wal_czynny-elementy_toczne-igielki.csv",
        "headers": [ "Kod", "D" ],
        "types": [ 'STRING', 'INTEGER']
    }
]

class DatabaseCreator:
    def __init__(self): 
        self._createDatabase()
        self._createTables()
        self._populateTables()

    def _createDatabase(self):
        # Get the destination directory absoulte path where csv and database files should be stored
        self._dataPath = DATA_PATH
        if not os.path.exists(DATA_PATH):
            sys.stderr.write(f"Error: {DATA_PATH} does not exist.\n")
            sys.exit(1)

        # Get the absoulte path of the created database
        self._databasePath = dependencies_path(f'{DATA_DIR_NAME}//baza_elementow.db')

        conn = sqlite3.connect(self._databasePath)
        conn.close
    
    def _createTables(self):
        conn = sqlite3.connect(self._databasePath)
        # Create table for every table parameters listed above
        self._tables = database_tables
        
        for table in self._tables:
            headersWithTypes = [h + ' ' + t for h, t in zip(table['headers'], table['types'])]
            headersStr = '", "'.join(headersWithTypes)
            query = f"CREATE TABLE IF NOT EXISTS \"{table['name']}\" ({headersStr})"
            conn.cursor().execute(query)

        conn.commit()
        conn.close
    
    def _populateTables(self):
        conn = sqlite3.connect(self._databasePath)
       
        for table in self._tables:
            # Get the associated csv file absolute path 
            csvPath = dependencies_path(f'{DATA_DIR_NAME}//{table["csvName"]}')
            # Check if the csv file exists
            if not os.path.exists(csvPath):
                sys.stderr.write(f"Error: {csvPath} does not exist.\n")
                conn.close()
                sys.exit(1)
            # Populate the table with data from the csv file
            df = pd.read_csv(csvPath, delimiter=';', decimal=',')
            df.columns = table["headers"]
            df.to_sql(table["name"], conn, if_exists='replace', index=False)

        conn.commit()
        conn.close()

dbCreator = DatabaseCreator()
