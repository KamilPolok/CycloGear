import sqlite3
import pandas as pd
import os
import sys

CURRENT_DIR_ABS_PATH = os.path.realpath(os.path.dirname(__file__))
DESTINATION_DIR_NAME = 'data'
DESTINATION_DIR_REL_PATH = os.path.join('..','..', DESTINATION_DIR_NAME)
DATABASE_NAME = 'baza_elementow.db'

database_tables = [
    {
        "item":  "łożyska",
        "group": "wał wejściowy",
        "type": "kulkowe",
        "name": "łożyska-wał wejściowy-kulkowe",
        "csvName": "wwe_kulkowe.csv",
        "headers": ["kod", "Dz", "Dw", "B", "C", "C0", "Vref", "Vdop"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']
    },
    {
        "item":  "łożyska",
        "group": "wał wejściowy",
        "type": "walcowe",
        "name": "łożyska-wał wejściowy-walcowe",
        "csvName": "wwe_walcowe.csv",
        "headers": ["kod", "Dz", "Dw", "B", "C", "C0", "Vref", "Vdop"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']
    },
    {
        "item":  "łożyska",
        "group": "tarcza",
        "type": "walcowe",
        "name": "łożyska-tarcza-walcowe",
        "csvName": "tarcza_walcowe.csv",
        "headers": ["kod", "Dz", "Dw", "B", "C", "C0", "Vref", "Vdop"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']
    },
    {
        "item":  "łożyska",
        "group": "tarcza",
        "type": "igiełkowe",
        "name": "łożyska-tarcza-igiełkowe",
        "csvName": "tarcza_igielkowe.csv",
        "headers": ["kod", "Dz", "Dw", "B", "C", "C0", "Vref", "Vdop"],
        "types": ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']
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
        # Get the absoulte destination directory path basing on its relative path
        destinationDirAbsPath = os.path.join(CURRENT_DIR_ABS_PATH, DESTINATION_DIR_REL_PATH)
        # Check if the absoulte destination directory path exists
        if not os.path.exists(destinationDirAbsPath):
            sys.stderr.write(f"Error: {destinationDirAbsPath} does not exist.\n")
            sys.exit(1)
        else:
            return destinationDirAbsPath
    
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
