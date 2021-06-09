from PySide6.QtWidgets import *

from Controller import ConfigurationRecordController, TopLevelController
from Controller.ConfigurationRecordController import ConfigurationRecordController

if __name__ == '__main__':
    # Create QApplication and QFrame instance
    app = QApplication([])
    top_controller = TopLevelController.Controller()

    # Try open SQLite configuration
    configuration_database = ConfigurationRecordController()
    if not configuration_database.connect_to_database():
        # Show the first time window
        top_controller.show_first_time()
    else:
        # TODO: set program settings based on database contents
        print("Opened configuration file.")
        settings = configuration_database.read_config()
        print("Home directory: %s" % settings['default_directory'])
        top_controller.show_welcome()

    app.exec()


# TODO:
#       Implement UI wireframes
#       Create unit tests for above functionality
