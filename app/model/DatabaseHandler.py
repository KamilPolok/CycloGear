import sqlite3
import pandas as pd
import os
import sys

CURRENT_DIR_ABS_PATH = os.path.realpath(os.path.dirname(__file__))
DESTINATION_DIR_NAME = 'data'
DESTINATION_DIR_REL_PATH = os.path.join('..','..', DESTINATION_DIR_NAME)
DATABASE_NAME = 'baza_elementow.db'

class DatabaseHandler:
    def __init__(self):
        self._startup()
    
    def _startup(self):
        # Check if destination folder where database file should be, exists
        destinationDirAbsPath = os.path.join(CURRENT_DIR_ABS_PATH, DESTINATION_DIR_REL_PATH)
        if not os.path.exists(destinationDirAbsPath):
            sys.stderr.write(f"Error: Directory {destinationDirAbsPath} does not exist.\n")
            sys.exit(1)
        # Check if database file exists
        self._databaseAbsPath = os.path.normpath(os.path.join(destinationDirAbsPath, DATABASE_NAME))
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
        headers = [column[1] for column in columns[1:]]

        conn.close()
        return headers

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
        headers = [column[1] for column in columns[1:]]

        conn.close()
        return {attribute:{"min": 0, "max": 0} for attribute in headers}

    # This function is currently not in use
    def getSingleItem(self, tableName, code):
        conn = sqlite3.connect(self._databaseAbsPath)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {tableName} WHERE KOD = {code}") 
        position = cursor.fetchone()

        conn.commit()
        conn.close()

        return position
    
    def getFilteredResults(self, tableName, limits):
        conn = sqlite3.connect(self._databaseAbsPath)
        # Create the base of the query
        query = f"SELECT * FROM \"{tableName}\" WHERE"
        # Create the filters query part
        filtersQuery = []

        for attribute, attributeLimits in limits.items():
                if attributeLimits['min']:
                    filtersQuery.append(f" \"{attribute}\" >= {attributeLimits['min']}")
                if attributeLimits['max']:
                    filtersQuery.append(f" \"{attribute}\" <= {attributeLimits['max']}")
        # Join the queries
        query += " AND".join(filtersQuery)

        if query.endswith(" AND") or query.endswith("WHERE"):
            query = query.rsplit(' ', 1)[0]
        # Get the results in form of a dataframe
        df = pd.read_sql_query(query,conn)

        conn.close()
        return df
    