import os.path
import sqlite3
from PyQt5.QtCore import *

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
        status (bool): database connection status
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

    def create_database(self, directory):
        try:
            self.conn = sqlite3.connect(self.database)
            self.cursor = self.conn.cursor()
        except IOError:
            print("Failed to create configuration record.")
            return

        # Insert table into database
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS config
                               (
                                attrib TEXT PRIMARY KEY,
                                value TEXT NOT NULL
                               );""")

        # Insert default directory into database
        self.cursor.execute("""INSERT INTO config (attrib, value)
                               VALUES(\'default_directory\', \'%s\')"""
                            % directory)

        # Commit changes
        self.conn.commit()

    def read_config(self):
        """
        Read program configuration from configuration file and return these settings.
        :return:
        settings (dict): Python dictionary of program settings read from config file
        """
        # Read data from settings database
        data = self.cursor.execute("""SELECT * FROM config""")

        # Create settings dictionary
        settings = {}
        for row in data:
            settings[row[0]] = row[1]

        # Return settings
        return settings

    def get_default_directory(self):
        """
        Get the program default directory from the configuration file.
        :return:
        file_path (str): file path of the program default directory
        """
        data = self.cursor.execute("""SELECT value from config WHERE attrib = \'default_directory\'""")
        for row in data:
            return row[0]