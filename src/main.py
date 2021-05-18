from os.path import expanduser
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from DirectoryManager import DirectoryManager


# Global variables (BAD, REMOVE)
home_dir = ""


def get_home_directory(label: QLabel):
    # Set home directory
    home_dir = expanduser("~")

    # Update label to output home directory
    label.setText(home_dir)


def create_directory(directory_name, msg):
    """ Determine the correct path to place hidden directory, in this case '.OnkoDICOM' """
    hidden_dir = DirectoryManager.determine_correct_path(directory_name)

    """ Create the path using the hidden_path we determined previously"""
    DirectoryManager.create_directory(hidden_dir)

    msg.exec_()



def remove_directory(directory_name, msg):
    """ Remove the path we just created """
    DirectoryManager.remove_directory(directory_name)

    msg.exec_()


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

    # Create QPushButton's to create directory and to remove directory
    button_create_dir = QPushButton("Create Directory")
    button_remove_dir = QPushButton("Remove Directory")

    # Create QMessageBox's to alert user of direction creation and removal
    msgBox_dir_creation = QMessageBox()
    msgBox_dir_removal = QMessageBox()

    # Set QMessageBox's properties
    msgBox_dir_creation.setWindowTitle("Attention")
    msgBox_dir_creation.setIcon(QMessageBox.Information)
    msgBox_dir_creation.setText("Please check your users directory for the created hidden directory. \nHint ('.OnkoDICOM')")
    msgBox_dir_removal.setWindowTitle("Attention")
    msgBox_dir_removal.setIcon(QMessageBox.Information)
    msgBox_dir_removal.setText("Please check your users directory for removal of hidden directory.")


    # Set widget properties
    home_dir_title_label.setFont(bold_font)
    home_dir_title_label.setAlignment(Qt.AlignCenter)
    home_dir_label.setAlignment(Qt.AlignCenter)

    # Add widgets to the layout
    layout.addWidget(button)
    layout.addWidget(home_dir_title_label)
    layout.addWidget(home_dir_label)

    layout.addWidget(button_create_dir)
    layout.addWidget(button_remove_dir)

    #Directory name
    dir_name = ".OnkoDICOM"

    # Display QMessageBox's respective to button press
    button_create_dir.clicked.connect(lambda: create_directory(dir_name, msgBox_dir_creation))
    button_remove_dir.clicked.connect(lambda: remove_directory(DirectoryManager.determine_correct_path(dir_name), msgBox_dir_removal))


    # When clicking the button, call function get_home_directory to update home_dir_label's text
    button.clicked.connect(lambda: get_home_directory(home_dir_label))

    # Show the window and run the application
    window.show()
    app.exec()


# TODO:
#       Implement UI wireframes
#       Create unit tests for above functionality
