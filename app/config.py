import os
import sys

# Set folder path relative to root of the application
def resource_path(relative_path):
    # Check if running as a bundled application
    if getattr(sys, 'frozen', False):
        # If bundled, the executable's directory is the base path
        base_path = os.path.dirname(sys.executable)
    else:
        # If running in a development environment, get 
        # path to root directory of repository - one directory level up
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    database_path = os.path.join(base_path, relative_path)
    return database_path

# Set data directory
DATA_DIR = 'data'
# Set database name
DATABASE_NAME = 'baza_elementow.db'

# Set path to data directory
DATA_PATH = resource_path(DATA_DIR)
