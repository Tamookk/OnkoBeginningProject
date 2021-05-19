from os.path import expanduser
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from DirectoryManager import DirectoryManager


# Global variables (BAD, REMOVE)
user_home = expanduser("~")
onko_folder = user_home


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


def show_file_browser(line_edit: QLineEdit, folder_model: QFileSystemModel):
    global onko_folder
    onko_folder = QFileDialog.getExistingDirectory(caption="Choose Directory", directory=user_home)
    if onko_folder == "":
        onko_folder = expanduser("~")
    line_edit.setText(onko_folder)
    folder_model.index(onko_folder)


if __name__ == '__main__':
    # Create QApplication and QFrame instance
    app = QApplication([])

    # Create bold font
    bold_font = QFont()
    bold_font.setBold(True)

    # Create window and layouts
    window = QWidget()
    window.setWindowTitle("Onko Beginning Project")
    outer_layout = QVBoxLayout()
    welcome_layout = QGridLayout()
    directory_layout = QGridLayout()
    folder_tree_layout = QGridLayout()
    window.setLayout(outer_layout)

    # Welcome widgets
    logo = QPixmap("../assets/images/logo.png")
    logo_label = QLabel()
    logo_label.setPixmap(logo)
    welcome_text = """
        Welcome to OnkoDICOM.\t\t\t\t\t\n
        Config file not found.\n
        Welcome message.\n
        Onko introduction.\n
        Onko missions.
        """
    welcome_text_label = QLabel(welcome_text)

    # Directory widgets
    directory_label = QLabel("Add a directory as your default directory")
    directory_input = QLineEdit()
    directory_input.setText(user_home)
    browse_button = QPushButton("Browse")

    # Folder tree widgets
    folder_model = QFileSystemModel()
    folder_model.setRootPath(user_home)
    folder_tree = QTreeView()
    folder_tree.setModel(folder_model)
    folder_tree.setCurrentIndex(folder_model.index(user_home))
    folder_tree.setAnimated(False)
    folder_tree.setIndentation(20)
    folder_tree.setSortingEnabled(True)
    folder_tree.setColumnWidth(0, folder_tree.width() * 0.3)
    skip_button = QPushButton("Skip")
    confirm_button = QPushButton("Confirm")

    # Message box for creating directory
    msgbox_create_dir = QMessageBox()
    msgbox_create_dir.setWindowTitle("Application Directory Created")
    msgbox_create_dir.setIcon(QMessageBox.Information)
    msgbox_create_dir.setText("Please check your users directory for the created hidden directory. \nHint ('.OnkoDICOM')")

    # Add widgets to welcome layout
    welcome_layout.addWidget(logo_label, 0, 0, 1, 1)
    welcome_layout.addWidget(welcome_text_label, 0, 1, 1, 3)

    # Add widgets to the directory layout
    directory_layout.addWidget(directory_label, 0, 0, 1, 4)
    directory_layout.addWidget(directory_input, 1, 0, 1, 3)
    directory_layout.addWidget(browse_button, 1, 3, 1, 1)

    # Add widgets to the folder tree layout
    folder_tree_layout.addWidget(folder_tree, 0, 0, 4, 4)
    folder_tree_layout.addWidget(skip_button, 4, 2, 1, 1)
    folder_tree_layout.addWidget(confirm_button, 4, 3, 1, 1)

    # Add widgets to the layout
    outer_layout.addLayout(welcome_layout)
    outer_layout.addLayout(directory_layout)
    outer_layout.addLayout(folder_tree_layout)

    # Attach functions to buttons
    browse_button.clicked.connect(lambda: show_file_browser(directory_input, folder_model))
    confirm_button.clicked.connect(lambda: create_directory(onko_folder, msgbox_create_dir))

    # Show the window and run the application
    window.show()
    app.exec()


# TODO:
#       Implement UI wireframes
#       Create unit tests for above functionality
