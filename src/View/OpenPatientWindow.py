from PySide6 import QtCore
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from Controller import ConfigurationRecordController, FindDICOMFileController
from os.path import expanduser


class OpenPatientWindow(QWidget):
    go_next_window = QtCore.Signal()
    go_previous_window = QtCore.Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Get default directory from configuration record
        self.database = ConfigurationRecordController.ConfigurationRecordController()
        self.database.connect_to_database()
        self.file_path = self.database.get_default_directory()

        # Create window and layouts
        self.window = QWidget()
        self.window.setWindowTitle("Select Patient Window")

        self.layout = QVBoxLayout()
        self.directory_layout = QGridLayout()
        self.tree_layout = QVBoxLayout()
        self.bottom_layout = QGridLayout()

        self.layout.addLayout(self.directory_layout)
        self.layout.addLayout(self.tree_layout)
        self.layout.addLayout(self.bottom_layout)
        self.window.setLayout(self.layout)

        # Directory widgets
        label_text = "Choose the path of the folder containing DICOM files to load Patient's details:"
        self.info_label = QLabel(label_text)
        self.directory_input = QLineEdit()
        self.directory_input.setText(self.file_path)
        self.directory_input.textChanged.connect(self.line_edit_changed)
        self.directory_input.returnPressed.connect(self.search_for_patient)
        self.browse_button = QPushButton("Browse")

        # Tree widgets
        self.patient_tree = QTreeWidget()
        self.patient_tree.setHeaderHidden(True)
        self.patient_tree.setHeaderLabels([""])

        # Bottom widgets
        self.bottom_text = "The selected directories above will be opened in the OnkoDICOM\nprogram. "
        self.bottom_text += "Click 'Refresh' to reload the files from the directory."
        self.bottom_label = QLabel(self.bottom_text)
        self.refresh_button = QPushButton("Refresh")
        self.back_button = QPushButton("Back")
        self.confirm_button = QPushButton("Confirm")

        # Add widgets to layout
        self.directory_layout.addWidget(self.info_label, 0, 0, 1, 4)
        self.directory_layout.addWidget(self.directory_input, 1, 0, 1, 3)
        self.directory_layout.addWidget(self.browse_button, 1, 3, 1, 1)

        self.tree_layout.addWidget(self.patient_tree)

        self.bottom_layout.addWidget(self.bottom_label, 0, 0, 2, 4)
        self.bottom_layout.addWidget(self.refresh_button, 2, 0, 1, 1)
        self.bottom_layout.addWidget(self.back_button, 2, 2, 1, 1)
        self.bottom_layout.addWidget(self.confirm_button, 2, 3, 1, 1)

        # Connect buttons to functions
        self.browse_button.clicked.connect(self.show_file_browser)
        self.back_button.clicked.connect(self.go_display_welcome_window)
        self.confirm_button.clicked.connect(self.go_display_image_window)
        #self.confirm_button.clicked.connect(self.search_for_patient)

    def line_edit_changed(self):
        """
        When the line edit box is changed, update related fields.
        """
        self.file_path = self.directory_input.text()

    def show_file_browser(self):
        """
        Show the file browser for selecting a folder for the Onko default directory.
        """
        # Open a file dialog and return chosen directory
        folder = QFileDialog.getExistingDirectory(caption="Choose Directory", directory=self.file_path)

        # If chosen directory is nothing (user clicked cancel) set to user home
        if folder == "":
            folder = expanduser("~")

        # Update file path
        self.file_path = folder

        # Update directory text
        self.directory_input.setText(self.file_path)

    def search_for_patient(self):
        """
        Searches for patient data inside the selected directory.
        """
        # Get the currently selected directory
        file_path = self.directory_input.text()

        # Start searching if the directory isn't empty
        if self.file_path != "":
            print("Searching")

        dicom_file_controller = FindDICOMFileController.FindDICOMFileController(file_path)
        dicom_file_controller.find_all_files()
        dicom_file_controller.find_DICOM_files()
        dicom_file_controller.check_elements()

    def go_display_welcome_window(self):
        """
        Go to previous window.
        """
        self.go_previous_window.emit()
        self.window.close()

    def go_display_image_window(self):
        """
        Go to the next window
        """
        self.search_for_patient()
        self.go_next_window.emit()
        self.window.close()

    def show(self):
        self.window.show()
