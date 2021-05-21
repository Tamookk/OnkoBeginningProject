import os.path
import sqlite3

class ConfigurationRecordController():
    def __init__(self):
        """
        Set up a database connection.
        """

        # Initialise class variables
        self.database = './configuration.record'
        self.conn = None
        self.cursor = None

    def connect_to_database(self):
        """
        Connect to a database.
        :return:
        status (bool)   : database connection status
        """
        if not os.path.exists(self.database):
            print("Configuration record not found.")
            return False

        try:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
            return True
        except IOError:
            print("Failed to open configuration record.")
            return False
