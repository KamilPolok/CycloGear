
import sqlite3
import pandas as pd
import os

class DatabaseHandler:

    def __init__(self):
        self._db_name = 'bearings.db'
        self._table_bb_name = 'ball_bearings'
        self._headers_list = ["KOD", "D WEWN", "D ZEWN", "B", "C", "C0", "V REF", "V DOP"]
        self._column_types = ['TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'REAL', 'REAL', 'INTEGER', 'INTEGER']


        self._csv_bb_name = 'lozyska_kulkowe.csv'
        self._csv_bb_path = os.path.normpath(os.path.join(os.path.realpath(os.path.dirname(__file__)),self._csv_bb_name))

        self._connection = None
        self._cursor = None

        self._create_database()
        self._populate_database()

    def _create_database(self):
        self._connection = sqlite3.connect(self._db_name)
        self._cursor = self._connection.cursor()

       
        headers_with_types = [h + ' ' + t for h, t in zip(self._headers_list, self._column_types)]
        headers_str = '", "'.join(headers_with_types)

        query = f"CREATE TABLE IF NOT EXISTS {self._table_bb_name} ({headers_str})"
        print(query)

        self._cursor.execute(query)
        
        self._connection.commit()
        self._connection.close()

    def _populate_database(self):
        self._connection = sqlite3.connect(self._db_name)
        self._cursor = self._connection.cursor()

        df = pd.read_csv(self._csv_bb_path, delimiter=';', decimal=',')
        df.columns = self._headers_list
        df.to_sql(self._table_bb_name, self._connection, if_exists='replace', index=False)

        self._connection.commit()
        self._connection.close()
    
    def get_attributes(self):
        attributes_list = self._headers_list
        attributes_list.pop(0)
        return attributes_list

    def get_single_position(self, code):
        self._connection = sqlite3.connect(self._db_name)
        self._cursor = self._connection.cursor()

        self._cursor.execute(f"SELECT * FROM {self._table_bb_name} WHERE KOD = {code}") 
        position = self._cursor.fetchone()

        self._connection.commit()
        self._connection.close()

        return position
        
    def get_filtered_table(self,limits):
        
        self._connection = sqlite3.connect(self._db_name)
        self._cursor = self._connection.cursor()

        query = f"SELECT * FROM {self._table_bb_name} WHERE"

        filter_conditions = []

        for key, limit in limits.items():
            if limit['min']:
                filter_conditions.append(f" \"{key}\" >= {limit['min']}")
            if limit['max']:
                filter_conditions.append(f" \"{key}\" <= {limit['max']}")
        
        query += " AND".join(filter_conditions)

        if query.endswith(" AND"):
            query = query.rsplit(' ', 1)[0]
        
        if query.endswith("WHERE"):
            query = query.rsplit(' ', 1)[0]

        df = pd.read_sql_query(query, self._connection)

        self._connection.close()

        return df