import sqlite3
import pandas as pd
import os

class Bearings1:
    def __init__(self):
        self.name = 'bearings1'
        self.headers = ["kod", "Dz", "Dw", "B", "C", "C0", "Vref", "Vdop"]
        self.types = ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']
        self.csvName = 'lozyska1.csv'

class Bearings2:
    def __init__(self):
        self.name = 'bearings2'
        self.headers = ["kod", "Dz", "Dw", "B", "C", "C0", "Vref", "Vdop"]
        self.types = ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']
        self.csvName = 'lozyska2.csv'

class Bearings3:
    def __init__(self):
        self.name = 'bearings3'
        self.headers = ["kod", "Dz", "Dw", "B", "C", "C0", "Vref", "Vdop"]
        self.types = ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']
        self.csvName = 'lozyska3.csv'

class DatabaseHandler:
    def __init__(self):
        self._tables = [Bearings1(), Bearings2(), Bearings3()]
        self._activeTable = None

        self._connection = None
        self._cursor = None

        self._findDbPath()
        
        self._createTables()
        self._populateDatabase()
    
    def _findDbPath(self):
        currentDirPath = os.path.realpath(os.path.dirname(__file__))
        dataDirName = 'data'
        dbName = 'bearings.db'
        self._dataDirPath = os.path.join(currentDirPath, '..', '..', dataDirName)
        self._dbPath = os.path.normpath(os.path.join(self._dataDirPath, dbName))

    def _createTables(self):
        self._connection = sqlite3.connect(self._dbPath)
        self._cursor = self._connection.cursor()

        for table in self._tables:
            headersWithTypes = [h + ' ' + t for h, t in zip(table.headers, table.types)]
            headersStr = '", "'.join(headersWithTypes)
            query = f"CREATE TABLE IF NOT EXISTS {table.name} ({headersStr})"
            self._cursor.execute(query)
        
        self._connection.commit()
        self._connection.close()

    def _populateDatabase(self):
        self._connection = sqlite3.connect(self._dbPath)
        self._cursor = self._connection.cursor()

        for table in self._tables:
            csvPath = os.path.normpath(os.path.join(self._dataDirPath,table.csvName))
            df = pd.read_csv(csvPath, delimiter=';', decimal=',')
            df.columns = table.headers
            df.to_sql(table.name, self._connection, if_exists='replace', index=False)

        self._connection.commit()
        self._connection.close()

    def getAvailableTables(self):
        return [table.name for table in self._tables]
    
    def setActiveTable(self, activeTableName):
        for table in self._tables:
            if table.name == activeTableName:
                self._activeTable = table

    def getActiveTable(self):
        return self._activeTable.name
    
    def getActiveTableAttributes(self):
        attributesList = self._activeTable.headers[1:]
        return attributesList
    
    def getFilterConditions(self):
        attributesList = self._activeTable.headers[1:]
        
        return {attribute:{"min": 0, "max": 0} for attribute in attributesList}

    def getSnglePosition(self, code):
        self._connection = sqlite3.connect(self._dbPath)
        self._cursor = self._connection.cursor()

        self._cursor.execute(f"SELECT * FROM {self._activeTable.name} WHERE KOD = {code}") 
        position = self._cursor.fetchone()

        self._connection.commit()
        self._connection.close()

        return position
        
    def getFilteredResults(self,limits):
        
        self._connection = sqlite3.connect(self._dbPath)
        self._cursor = self._connection.cursor()

        query = f"SELECT * FROM {self._activeTable.name} WHERE"

        filterConditions = []

        for attribute, attributeLimits in limits.items():
                if attributeLimits['min']:
                    filterConditions.append(f" \"{attribute}\" >= {attributeLimits['min']}")
                if attributeLimits['max']:
                    filterConditions.append(f" \"{attribute}\" <= {attributeLimits['max']}")
            
        query += " AND".join(filterConditions)

        if query.endswith(" AND") or query.endswith("WHERE"):
            query = query.rsplit(' ', 1)[0]
        

        df = pd.read_sql_query(query, self._connection)

        self._connection.close()

        return df
