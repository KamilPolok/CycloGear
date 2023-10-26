import sqlite3
import pandas as pd
import os
import sys


root_directory = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                               '..', '..', '..',))
sys.path.append(root_directory)


from config import DATA_DIR, DATABASE_NAME

database_tables = [
    {
        "item":  "łożyska",
        "group": "wał wejściowy",
        "type": "kulkowe",
        "name": "łożyska-wał wejściowy-kulkowe",
        "csvName": "wwe_kulkowe.csv",
        "headers": ["kod", "Dw [mm]", "Dz [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER']
    },
    {
        "item":  "łożyska",
        "group": "wał wejściowy",
        "type": "walcowe",
        "name": "łożyska-wał wejściowy-walcowe",
        "csvName": "wwe_walcowe.csv",
        "headers": ["kod", "Dw [mm]", "Dz [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER']
    },
    {
        "item":  "łożyska",
        "group": "tarcza",
        "type": "walcowe",
        "name": "łożyska-tarcza-walcowe",
        "csvName": "tarcza_walcowe.csv",
        "headers": ["kod", "Dw [mm]", "E [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]"],
        "types": ['TEXT', 'INTEGER', 'REAL', 'INTEGER', 'REAL', 'REAL', 'INTEGER']
    },
    {
        "item":  "łożyska",
        "group": "tarcza",
        "type": "igiełkowe",
        "name": "łożyska-tarcza-igiełkowe",
        "csvName": "tarcza_igielkowe.csv",
        "headers": ["kod", "Dw [mm]", "E [mm]", "B [mm]", "C [kN]", "C0 [kN]", "n max [obr/min]"],
        "types": ['TEXT', 'INTEGER', 'REAL', 'INTEGER', 'REAL', 'REAL', 'INTEGER']
    },
]

class DatabaseCreator:
    def __init__(self):
        self._createDatabase()
        self._createTables()
        self._populateTables()

    def _createDatabase(self):
        # Get the destination directory absoulte path where csv and database files shuld be stored
        self._destinationDirAbsPath = self._findDestinationDirectory()
        # Get the absoulte path of the created database
        self._databaseAbsPath = os.path.normpath(os.path.join(self._destinationDirAbsPath, DATABASE_NAME))

        conn = sqlite3.connect(self._databaseAbsPath)
        conn.close

    def _findDestinationDirectory(self):
        if not os.path.exists(DATA_DIR):
            sys.stderr.write(f"Error: {DATA_DIR} does not exist.\n")
            sys.exit(1)
        else:
            return DATA_DIR
    
    def _createTables(self):
        conn = sqlite3.connect(self._databaseAbsPath)
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
        conn = sqlite3.connect(self._databaseAbsPath)
       
        for table in self._tables:
            # Get the associated csv file absolute path 
            csvPath = os.path.normpath(os.path.join(self._destinationDirAbsPath,table["csvName"]))
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
