import unittest
import os, sys
from os.path import expanduser
import platform
import sqlite3
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from Controller import ConfigurationRecordController
from Controller.ConfigurationRecordController import ConfigurationRecordController


def get_home_directory():
    """ Set home directory """
    return expanduser("~")


def get_system():
    """ Returns the location of the config file depending on the system """
    if platform.system() == "Windows":
        database = ".\configuration.record"
        return database
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        database = "./configuration.record"
        return database
    else:
        print("System not recognised. \nOnkoDICOM only supported on Linux, Windows & OS X systems.")
        exit()


def create_record():
    """ Checks the OS of the user to determine where to create the config file """
    database = get_system()
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
    except IOError:
        print("Failed to create configuration record.")
        return

    # Insert table into database
    cursor.execute("""CREATE TABLE IF NOT EXISTS config
                           (
                            attrib TEXT PRIMARY KEY,
                            value TEXT NOT NULL
                           );""")
    # Commit changes
    conn.commit()


def write_record():
    """
    Checks the OS of the user to determine how to locate the config file
    Don't think this prevents SQL injection
    """
    database = get_system()
    if platform.system() == "Windows":
        directory = get_home_directory() + "\\.OnkoDICOM\\"
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        directory = get_home_directory() + "/.OnkoDICOM/"

    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
    except IOError:
        print("Failed to create configuration record.")
        return

    # Insert default dir into the table
    cursor.execute("""INSERT INTO config (attrib, value)
                                   VALUES(\'default_directory\', \'%s\')"""
                   % directory)
    # Commit changes
    conn.commit()


def check_row_exists():
    """ Checks if the default_directory row exists and returns true """
    database = get_system()
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
    except IOError:
        print("Failed to create configuration record.")
        return
    return cursor.execute("""SELECT EXISTS (SELECT value from config WHERE attrib = \'default_directory\')""")


def read_record():
    """ Reads the default_directory row and returns the value """
    database = get_system()
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
    except IOError:
        print("Failed to create configuration record.")
        return
    data = cursor.execute("""SELECT value from config WHERE attrib = \'default_directory\'""")
    for row in data:
        return row[0]


class Test01CreateRecord(unittest.TestCase):
    """ Test that the SQL file is created """
    def test_create_record(self):
        create_record()
        self.assertTrue(os.path.isfile("configuration.record"))


class Test02WriteRecord(unittest.TestCase):
    """ Test that the record file can be written to """
    def test_write_record(self):
        write_record()
        self.assertTrue(check_row_exists())


class Test03ReadRecord(unittest.TestCase):
    """
    Test that the file can be read (eg. isn't corrupted)
    Set the 'a' to be default home directory and 'b' as the directory read from .record
    """
    def test_read_record(self):
        config = ConfigurationRecordController()
        config.connect_to_database()
        if platform.system() == "Windows":
            a = get_home_directory() + "\\.OnkoDICOM\\"
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            a = get_home_directory() + "/.OnkoDICOM/"
        b = read_record()
        self.assertEqual(a, b)


unittest.main(argv=[''], verbosity=2, exit=False)
os.remove("configuration.record")