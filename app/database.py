import sqlite3
import pandas as pd
import os

class DatabaseHandler:

    def __init__(self):
        self._dbName = 'bearings.db'
        self._tableBbName = 'ball_bearings'
        self._tableBbHeaderList = ["KOD", "D WEWN", "D ZEWN", "B", "C", "C0", "V REF", "V DOP"]
        self._tableBbColumnTypes = ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']


        self._csvBbName = 'lozyska_kulkowe.csv'
        self._csvBbPath = os.path.normpath(os.path.join(os.path.realpath(os.path.dirname(__file__)),self._csvBbName))

        self._connection = None
        self._cursor = None

        self._createDatabase()
        self._populateDatabase()

    def _createDatabase(self):
        self._connection = sqlite3.connect(self._dbName)
        self._cursor = self._connection.cursor()

       
        headersWithTypes = [h + ' ' + t for h, t in zip(self._tableBbHeaderList, self._tableBbColumnTypes)]
        headersStr = '", "'.join(headersWithTypes)

        query = f"CREATE TABLE IF NOT EXISTS {self._tableBbName} ({headersStr})"

        self._cursor.execute(query)
        
        self._connection.commit()
        self._connection.close()

    def _populateDatabase(self):
        self._connection = sqlite3.connect(self._dbName)
        self._cursor = self._connection.cursor()

        df = pd.read_csv(self._csvBbPath, delimiter=';', decimal=',')
        df.columns = self._tableBbHeaderList
        df.to_sql(self._tableBbName, self._connection, if_exists='replace', index=False)

        self._connection.commit()
        self._connection.close()
    
    def getFilterConditions(self):
        attributesList = self._tableBbHeaderList
        attributesList.pop(0)
        
        return {attribute:{"min": 0, "max": 0} for attribute in self._tableBbHeaderList}

    def getSnglePosition(self, code):
        self._connection = sqlite3.connect(self._dbName)
        self._cursor = self._connection.cursor()

        self._cursor.execute(f"SELECT * FROM {self._tableBbName} WHERE KOD = {code}") 
        position = self._cursor.fetchone()

        self._connection.commit()
        self._connection.close()

        return position
        
    def getFilteredResults(self,limits):
        
        self._connection = sqlite3.connect(self._dbName)
        self._cursor = self._connection.cursor()

        query = f"SELECT * FROM {self._tableBbName} WHERE"

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