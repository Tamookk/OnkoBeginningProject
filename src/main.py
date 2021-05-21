from os.path import expanduser
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from DirectoryManager import DirectoryManager
from GUI.FirstTimeWindow import FirstTimeWindow


if __name__ == '__main__':
    # Create QApplication and QFrame instance
    app = QApplication([])

    # Show the window and run the application
    window = FirstTimeWindow()
    window.show()
    app.exec()


# TODO:
#       Implement UI wireframes
#       Create unit tests for above functionality
