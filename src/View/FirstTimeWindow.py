from Controller.ConfigurationRecordController import ConfigurationRecordController
from DirectoryManager import DirectoryManager
#from PyQt5 import QtCore
from os.path import exists, expanduser
from PySide6 import QtCore
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class FirstTimeWindow(QWidget):
    go_next_window = QtCore.Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Create class variables
        self.user_home = expanduser("~")
        self.onko_folder = self.user_home

        # Create window and layouts
        self.window = QWidget()
        self.window.setWindowTitle("Onko Beginning Project")
        self.outer_layout = QVBoxLayout()
        self.welcome_layout = QGridLayout()
        self.directory_layout = QGridLayout()
        self.folder_tree_layout = QGridLayout()
        self.window.setLayout(self.outer_layout)

        # Welcome widgets
        self.logo = QPixmap("../assets/images/logo.png")
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo)
        self.welcome_text = """
                Welcome to OnkoDICOM.\t\t\t\t\t\n
                Config file not found.\n
                Welcome message.\n
                Onko introduction.\n
                Onko missions.
                """
        self.welcome_text_label = QLabel(self.welcome_text)

        # Directory widgets
        self.directory_label = QLabel("Add a directory as your default directory")
        self.directory_input = QLineEdit()
        self.directory_input.setText(self.user_home)
        self.directory_input.textChanged.connect(lambda: self.line_edit_changed())
        self.browse_button = QPushButton("Browse")

        # Folder tree widgets
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath(self.onko_folder)
        self.folder_tree = QTreeView()
        self.folder_tree.setModel(self.folder_model)
        self.folder_tree.setCurrentIndex(self.folder_model.index(self.onko_folder))
        self.folder_tree.setAnimated(False)
        self.folder_tree.setIndentation(20)
        self.folder_tree.setSortingEnabled(True)
        self.folder_tree.setColumnWidth(0, self.folder_tree.width() * 0.3)
        self.skip_button = QPushButton("Skip")
        self.confirm_button = QPushButton("Confirm")

        # Message box for creating directory
        self.msgbox_create_dir = QMessageBox()
        self.msgbox_create_dir.setWindowTitle("Application Directory Created")
        self.msgbox_create_dir.setIcon(QMessageBox.Information)
        self. msgbox_create_dir.setText(
            "Please check your users directory for the created hidden directory. \nHint ('.OnkoDICOM')")

        # Add widgets to welcome layout
        self.welcome_layout.addWidget(self.logo_label, 0, 0, 1, 1)
        self.welcome_layout.addWidget(self.welcome_text_label, 0, 1, 1, 3)

        # Add widgets to the directory layout
        self.directory_layout.addWidget(self.directory_label, 0, 0, 1, 4)
        self.directory_layout.addWidget(self.directory_input, 1, 0, 1, 3)
        self.directory_layout.addWidget(self.browse_button, 1, 3, 1, 1)

        # Add widgets to the folder tree layout
        self.folder_tree_layout.addWidget(self.folder_tree, 0, 0, 4, 4)
        self.folder_tree_layout.addWidget(self.skip_button, 4, 2, 1, 1)
        self.folder_tree_layout.addWidget(self.confirm_button, 4, 3, 1, 1)

        # Add widgets to the layout
        self.outer_layout.addLayout(self.welcome_layout)
        self.outer_layout.addLayout(self.directory_layout)
        self.outer_layout.addLayout(self.folder_tree_layout)

        # Attach functions to buttons
        self.browse_button.clicked.connect(lambda: self.show_file_browser())
        self.confirm_button.clicked.connect(lambda: self.create_directory())

    def line_edit_changed(self):
        """
        When the line edit box is changed, update related fields.
        """
        temp_dir = ""

        # Set the field to the user's home if they make it empty
        if self.directory_input.text() == "":
            temp_dir = expanduser("~")
        else:
            temp_dir = self.directory_input.text()
            self.directory_input.setText(temp_dir)

        # Update onko folder
        self.onko_folder = temp_dir

        # Update directory text and tree view
        self.folder_model.setRootPath(self.onko_folder)
        self.folder_tree.setCurrentIndex(self.folder_model.index(self.onko_folder))

    def show_file_browser(self):
        """
        Show the file browser for selecting a folder for the Onko default directory.
        """

        # Open a file dialog and return chosen directory
        self.onko_folder = QFileDialog.getExistingDirectory(caption="Choose Directory", directory=self.user_home)

        # If chosen directory is nothing (user clicked cancel) set to user home
        if self.onko_folder == "":
            self.onko_folder = expanduser("~")

        # Update directory text and tree view
        self.directory_input.setText(self.onko_folder)
        self.folder_model.setRootPath(self.onko_folder)
        self.folder_tree.setCurrentIndex(self.folder_model.index(self.onko_folder))

    def create_directory(self):
        """
        Create the hidden application directory, '.OnkoDICOM'.
        """
        if not exists(self.onko_folder):
            self.onko_folder = expanduser("~")
            self.directory_input.setText(self.onko_folder)
            self.folder_model.setRootPath(self.onko_folder)
            self.folder_tree.setCurrentIndex(self.folder_model.index(self.onko_folder))

        # Determine the default directory path
        hidden_dir = DirectoryManager.determine_correct_path(self.onko_folder)

        # Create the application directory
        DirectoryManager.create_directory(hidden_dir)

        # Create database and insert hidden directory
        config_controller = ConfigurationRecordController()
        config_controller.create_database(hidden_dir)

        # Tell the user the directory has been created
        self.msgbox_create_dir.exec_()
        self.go_open_patient_window()
        self.window.close()

    def remove_directory(self):
        """
        Remove the application directory.
        """
        DirectoryManager.remove_directory(self.onko_folder)

        # Tell the user the directory has been deleted
        self.msgbox_create_dir.exec_()

    def go_open_patient_window(self):
        """
        Go to the next window
        """
        self.go_next_window.emit()

    def show(self):
        self.window.show()
