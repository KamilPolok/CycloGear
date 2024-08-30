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
        self._database_abs_path = dependencies_path(f'{DATA_DIR_NAME}//baza_elementow.db')
        if not os.path.exists(self._database_abs_path):
            sys.stderr.write(f"Error: Database file {self._database_abs_path} does not exist.\n")
            sys.exit(1)
        # Check the connection with the database
        try:
            conn = sqlite3.connect(self._database_abs_path)
            conn.close()
        except sqlite3.Error as e:
            sys.stderr.write(f"Connection failed with error: {e}")
        #TODO: Add check if all required tables are in the database and check if they aren't empty

    def get_available_tables(self, table_group_name = None):
        conn = sqlite3.connect(self._database_abs_path)
        cursor = conn.cursor()
        # Fetch all tables names from the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = [row[0] for row in cursor.fetchall()]
        # If table group name is not provided, return all tables 
        if table_group_name is None:
            return all_tables
        else:
            # Filter tables based on the provided table group name
            matching_table_names = [table for table in all_tables if table.startswith(table_group_name)]

            if not matching_table_names:
                sys.stderr.write(f"Error: Invalid group name: {table_group_name}.\n")
                conn.close()
                return []

            conn.close()
            return matching_table_names
    
    def get_table_items_attributes(self, table_name):
        conn = sqlite3.connect(self._database_abs_path)
        cursor = conn.cursor()
        # Check if the table exists in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            sys.stderr.write(f"Table '{table_name}' does not exist in the database.")
            conn.close()
            return []
        # Get the column names from the table and store them in list
        cursor.execute(f"PRAGMA table_info(\"{table_name}\")")
        columns =  cursor.fetchall()

        conn.close()

        headers = [column[1] for column in columns[1:]]

        attributes = [(header.split('[')[0].strip(), header[header.find('[')+1:header.find(']')].strip()) for header in headers]
        return attributes

    def get_table_items_filters(self, table_or_group_name):
        conn = sqlite3.connect(self._database_abs_path)
        cursor = conn.cursor()
        # First, try to treat the input as a full table name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_or_group_name,))
        table = cursor.fetchone()
        # If not found, then try to treat the input as a group name prefix
        if not table:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ? LIMIT 1", (table_or_group_name + '%',))
            table = cursor.fetchone()
        # Check if any table with given name or group name prefix was found
        if not table:
            sys.stderr.write(f"No tables found with name or group name: {table_or_group_name}.")
            conn.close()
            return []
        # Get the column names from the table and store them in list
        cursor.execute(f"PRAGMA table_info(\"{table[0]}\")")
        columns = cursor.fetchall()

        column_names = [column[1] for column in columns[1:]]
        # Get only the attributse from the column names 
        attributes = [re.sub(r'\[.*?\]', '', name).strip() for name in column_names]

        conn.close()
        return {attribute:{"min": 0, "max": 0} for attribute in attributes}

    def get_single_item(self, table_name, code):
        conn = sqlite3.connect(self._database_abs_path)
        cursor = conn.cursor()

        # Get the columns names
        cursor.execute(f"PRAGMA table_info(\"{table_name}\")")
        columns = cursor.fetchall()

        # Set the dictionary - for every name in the column name create a list with values and units.
        attributes = {}

        for column in columns:
            coulmn_name = column[1]
            # Check if the item contains square brackets (indicating a unit)
            if '[' in coulmn_name and ']' in coulmn_name:
                # Split the attribute and its unit
                attr, unit = coulmn_name.rsplit(' ', 1)
                # Remove the square brackets from the unit
                unit = unit.strip('[]')
            else:
                # For items without a unit, use the whole item as the attribute and an empty string for the unit
                attr, unit = coulmn_name, ''

            # Add to the dictionary
            attributes[attr] = [None, unit]
        # Get the first column name
        first_column_name = columns[0][1]

        # Find the row where the first column is equal to code
        cursor.execute(f"SELECT * FROM \"{table_name}\" WHERE {first_column_name} = ?", (code,)) 
        item_data = cursor.fetchone()

        # For every value in the row get the adequate column name and set the value in the list
        for i, value in enumerate(item_data):
            attribute = list(attributes.keys())[i]
            attributes[attribute][0] = value
        
        conn.close()

        return attributes
    
    def get_filtered_results(self, table_name, limits):
        conn = sqlite3.connect(self._database_abs_path)
        cursor = conn.cursor()

        # Check if the table exists in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            sys.stderr.write(f"Table '{table_name}' does not exist in the database.")
            conn.close()
            return []

        # Get the column names from the table and store them in list
        cursor.execute(f"PRAGMA table_info(\"{table_name}\")")
        columns =  cursor.fetchall()

        column_names = [column[1] for column in columns[1:]]
        # Create the base of the query
        query = f"SELECT * FROM \"{table_name}\" WHERE"
        # Create the filters query part
        filters_query = []

        for attribute, attribute_limits in limits.items():
                # Get the full column name from the header of the table: attribute + units part
                column_name = next((column_name for column_name in column_names if column_name.startswith(attribute)), None)
                if attribute_limits['min']:
                    filters_query.append(f" \"{column_name}\" >= {attribute_limits['min']}")
                if attribute_limits['max']:
                    filters_query.append(f" \"{column_name}\" <= {attribute_limits['max']}")
        # Join the queries
        query += " AND".join(filters_query)

        if query.endswith(" AND") or query.endswith("WHERE"):
            query = query.rsplit(' ', 1)[0]
        # Get the results in form of a dataframe
        df = pd.read_sql_query(query,conn)

        conn.close()
        df.columns = [column.replace("[", "\n[") for column in df.columns]
        return df
