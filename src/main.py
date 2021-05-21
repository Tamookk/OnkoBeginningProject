from os.path import expanduser
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *

from Controller.ConfigurationRecordController import ConfigurationRecordController
from GUI.FirstTimeWindow import FirstTimeWindow

if __name__ == '__main__':
    # Create QApplication and QFrame instance
    app = QApplication([])



    # Try open SQLite configuration
    configuration_database = ConfigurationRecordController()
    if not configuration_database.connect_to_database():
        # Show the first time window
        window = FirstTimeWindow()
        window.show()
    else:
        # TODO: set program settings based on database contents
        print("Opened configuration file.")
        settings = configuration_database.read_config()
        print("Home directory: %s" % settings['default_directory'])
        exit()

    app.exec()


# TODO:
#       Implement UI wireframes
#       Create unit tests for above functionality
