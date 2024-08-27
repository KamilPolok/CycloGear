import sqlite3
import pandas as pd
import os
import sys
import re

from config import DATA_PATH, DATA_DIR_NAME, dependencies_path

class DatabaseHandler:
    def __init__(self):
        self._startup()
    
    def _startup(self):
        # Check if destination folder where database file should be, exists
        if not os.path.exists(DATA_PATH):
            sys.stderr.write(f"Error: Directory {DATA_PATH} does not exist.\n")
            sys.exit(1)
        # Check if database file exists
        self._databaseAbsPath = dependencies_path(f'{DATA_DIR_NAME}//baza_elementow.db')
        if not os.path.exists(self._databaseAbsPath):
            sys.stderr.write(f"Error: Database file {self._databaseAbsPath} does not exist.\n")
            sys.exit(1)
        # Check the connection with the database
        try:
            conn = sqlite3.connect(self._databaseAbsPath)
            conn.close()
        except sqlite3.Error as e:
            print(f"Connection failed with error: {e}")
        #TODO: Add check if all required tables are in the database and check if they aren't empty

    def getAvailableTables(self, tableGroupName = None):
        conn = sqlite3.connect(self._databaseAbsPath)
        cursor = conn.cursor()
        # Fetch all tables names from the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        allTables = [row[0] for row in cursor.fetchall()]
        # If table group name is not provided, return all tables 
        if tableGroupName is None:
            return allTables
        else:
            # Filter tables based on the provided table group name
            matchingTableNames = [table for table in allTables if table.startswith(tableGroupName)]

            if not matchingTableNames:
                sys.stderr.write(f"Error: Invalid group name: {tableGroupName}.\n")
                conn.close()
                return []

            conn.close()
            return matchingTableNames
    
    def getTableItemsAttributes(self, tableName):
        conn = sqlite3.connect(self._databaseAbsPath)
        cursor = conn.cursor()
        # Check if the table exists in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tableName,))
        if not cursor.fetchone():
            sys.stderr.write(f"Table '{tableName}' does not exist in the database.")
            conn.close()
            return []
        # Get the column names from the table and store them in list
        cursor.execute(f"PRAGMA table_info(\"{tableName}\")")
        columns =  cursor.fetchall()

        conn.close()

        headers = [column[1] for column in columns[1:]]

        attributes = [(header.split('[')[0].strip(), header[header.find('[')+1:header.find(']')].strip()) for header in headers]
        return attributes

    def getTableItemsFilters(self, tableOrGroupName):
        conn = sqlite3.connect(self._databaseAbsPath)
        cursor = conn.cursor()
        # First, try to treat the input as a full table name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tableOrGroupName,))
        table = cursor.fetchone()
        # If not found, then try to treat the input as a group name prefix
        if not table:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ? LIMIT 1", (tableOrGroupName + '%',))
            table = cursor.fetchone()
        # Check if any table with given name or group name prefix was found
        if not table:
            sys.stderr.write(f"No tables found with name or group name: {tableOrGroupName}.")
            conn.close()
            return []
        # Get the column names from the table and store them in list
        cursor.execute(f"PRAGMA table_info(\"{table[0]}\")")
        columns = cursor.fetchall()

        columnNames = [column[1] for column in columns[1:]]
        # Get only the attributse from the column names 
        attributes = [re.sub(r'\[.*?\]', '', name).strip() for name in columnNames]

        conn.close()
        return {attribute:{"min": 0, "max": 0} for attribute in attributes}

    def getSingleItem(self, tableName, code):
        conn = sqlite3.connect(self._databaseAbsPath)
        cursor = conn.cursor()

        # Get the columns names
        cursor.execute(f"PRAGMA table_info(\"{tableName}\")")
        columns = cursor.fetchall()

        # Set the dictionary - for every name in the column name create a list with values and units.
        attributes = {}

        for column in columns:
            coulmnName = column[1]
            # Check if the item contains square brackets (indicating a unit)
            if '[' in coulmnName and ']' in coulmnName:
                # Split the attribute and its unit
                attr, unit = coulmnName.rsplit(' ', 1)
                # Remove the square brackets from the unit
                unit = unit.strip('[]')
            else:
                # For items without a unit, use the whole item as the attribute and an empty string for the unit
                attr, unit = coulmnName, ''

            # Add to the dictionary
            attributes[attr] = [None, unit]
        # Get the first column name
        FirstColumnName = columns[0][1]

        # Find the row where the first column is equal to code
        cursor.execute(f"SELECT * FROM \"{tableName}\" WHERE {FirstColumnName} = ?", (code,)) 
        itemData = cursor.fetchone()

        # For every value in the row get the adequate column name and set the value in the list
        for i, value in enumerate(itemData):
            attribute = list(attributes.keys())[i]
            attributes[attribute][0] = value
        
        conn.close()

        return attributes
    
    def getFilteredResults(self, tableName, limits):
        conn = sqlite3.connect(self._databaseAbsPath)
        cursor = conn.cursor()

        # Check if the table exists in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tableName,))
        if not cursor.fetchone():
            sys.stderr.write(f"Table '{tableName}' does not exist in the database.")
            conn.close()
            return []

        # Get the column names from the table and store them in list
        cursor.execute(f"PRAGMA table_info(\"{tableName}\")")
        columns =  cursor.fetchall()

        columnNames = [column[1] for column in columns[1:]]
        # Create the base of the query
        query = f"SELECT * FROM \"{tableName}\" WHERE"
        # Create the filters query part
        filtersQuery = []

        for attribute, attributeLimits in limits.items():
                # Get the full column name from the header of the table: attribute + units part
                columnName = next((columnName for columnName in columnNames if columnName.startswith(attribute)), None)
                if attributeLimits['min']:
                    filtersQuery.append(f" \"{columnName}\" >= {attributeLimits['min']}")
                if attributeLimits['max']:
                    filtersQuery.append(f" \"{columnName}\" <= {attributeLimits['max']}")
        # Join the queries
        query += " AND".join(filtersQuery)

        if query.endswith(" AND") or query.endswith("WHERE"):
            query = query.rsplit(' ', 1)[0]
        # Get the results in form of a dataframe
        df = pd.read_sql_query(query,conn)

        conn.close()
        df.columns = [column.replace("[", "\n[") for column in df.columns]
        return df
