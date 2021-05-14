from os.path import expanduser
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


# Global variables (BAD, REMOVE)
home_dir = ""


def get_home_directory(label: QLabel):
    # Set home directory
    home_dir = expanduser("~")

    # Update label to output home directory
    label.setText(home_dir)


if __name__ == '__main__':
    # Create QApplication and QFrame instance
    app = QApplication([])

    # Create bold font
    bold_font = QFont()
    bold_font.setBold(True)

    # Create window and vertical layout
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    # Create a QPushButton and QLabels to get and show user home
    button = QPushButton("Discover Home Directory")
    home_dir_title_label = QLabel("Home Directory")
    home_dir_label = QLabel("")

    # Set widget properties
    home_dir_title_label.setFont(bold_font)
    home_dir_title_label.setAlignment(Qt.AlignCenter)
    home_dir_label.setAlignment(Qt.AlignCenter)

    # Add widgets to the layout
    layout.addWidget(button)
    layout.addWidget(home_dir_title_label)
    layout.addWidget(home_dir_label)

    # When clicking the button, call function get_home_directory to update home_dir_label's text
    button.clicked.connect(lambda: get_home_directory(home_dir_label))

    # Show the window and run the application
    window.show()
    app.exec()


# TODO: 
#       Access hidden application directory (create if not present)
#       Implement UI wireframes
#       Create unit tests for above functionality
