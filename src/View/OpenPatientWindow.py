from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Controller import ConfigurationRecordController, FindDICOMFileController
from os.path import expanduser

import platform


class OpenPatientWindow(QWidget):
    go_next_window = QtCore.pyqtSignal()
    go_previous_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Get default directory from configuration record
        self.database = ConfigurationRecordController.ConfigurationRecordController()
        self.database.connect_to_database()
        self.file_path = self.database.get_default_directory()

        # DICOM file controller
        self.dicom_file_controller = FindDICOMFileController.FindDICOMFileController(self.file_path)

        # Dictionary of DICOM files
        self.DICOM_files = {}

        # Create window and layouts
        self.window = QWidget()
        self.window.setWindowTitle("Onko Beginning Project")
        self.window.resize(840, 530)

        self.layout = QVBoxLayout()
        self.directory_layout = QGridLayout()
        self.tree_layout = QVBoxLayout()
        self.bottom_layout = QGridLayout()

        self.layout.addLayout(self.directory_layout)
        self.layout.addLayout(self.tree_layout)
        self.layout.addLayout(self.bottom_layout)
        self.window.setLayout(self.layout)
        self.layout.setAlignment(Qt.Qt.AlignCenter)

        # Window stylesheet
        self.stylesheet = """
            QLineEdit
            {
                padding: 0 16px;
                min-height: 36px;
            }
            
            QPushButton
            {
                margin: 4px;
                padding: 0 16px;
                min-height: 36px;
                border-radius: 2px;
                color: #f5f5f5;
                font-family: "Segoe UI", "Roboto", "Helvetica Neue", sans-serif;
                font-size: 14px;
                text-align: center;
                qproperty-iconSize: 18px;
            }
            QPushButton#NormalButton
            {
                background-color: #9370db;
            }
            QPushButton#NormalButton:hover
            {   
                /* +10% saturation */
                background-color: #b299e6;
            }
            QPushButton#NormalButton:pressed
            {
                /* -20% saturation */
                background-color: #5c2eb8;
            }
            QPushButton#ConfirmButton
            {
                background-color: #388e3c;
            }
            QPushButton#ConfirmButton:hover
            {
                background-color: #49b64e;
            }
            QPushButton#ConfirmButton:pressed
            {
                background-color: #1d491f;
            }
            QPushButton#SkipButton
            {
                background-color: #f44336;
            }
            QPushButton#SkipButton:hover
            {
                background-color: #f7776e;
            }
            QPushButton#SkipButton:pressed
            {
                background-color: #c2160a;
            }
            
            QTreeView::item
            {
                color: #000000;
                min-height: 36px;
                font-size: 16px;
            }
            QTreeView::item:hover:!focus
            {
                background-color: #b299e6;
            }
            QTreeView::item:focus:!hover
            {
                border: 2px solid #9370DB;
            }
            QTreeView::item:selected:hover:!focus, QTreeView::item:selected:hover
            {
                background-color: #5c2eb8;
                color: white;
                border: 2px solid rgb(200, 200, 200);
            }
            QTreeView::item:selected:!hover:focus
            {
                background-color: #5c2eb8;
                color: white;
                border: 2px solid #9370DB;
            }
            """

        # Directory widgets
        label_text = "Change the directory to another folder containing DICOM files to load patient's details:"
        self.label_font = QFont()
        self.label_font.setPixelSize(14)
        self.info_label = QLabel(label_text)
        self.info_label.setFont(self.label_font)
        self.directory_input = QLineEdit()
        self.directory_input.setText(self.file_path)
        self.directory_input.textChanged.connect(self.line_edit_changed)
        self.directory_input.returnPressed.connect(self.search_for_patient)

        self.browse_button = QPushButton("Change")
        self.browse_button.setObjectName("NormalButton")
        self.browse_button.setStyleSheet(self.stylesheet)
        self.directory_input.setStyleSheet(self.stylesheet)

        # Tree widgets
        self.patient_tree = QTreeWidget()
        self.patient_tree.setHeaderLabels(["File Name", "File Type"])
        self.patient_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.patient_tree.setStyleSheet(self.stylesheet)

        # Bottom widgets
        self.bottom_text = "The selected directories above will be opened in the OnkoDICOM program. "
        self.bottom_text += "Click 'Refresh' to reload the files from the directory."
        self.bottom_label = QLabel(self.bottom_text)
        self.bottom_label.setFont(self.label_font)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setObjectName("NormalButton")
        self.refresh_button.setStyleSheet(self.stylesheet)
        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("SkipButton")
        self.back_button.setStyleSheet(self.stylesheet)
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setObjectName("ConfirmButton")
        self.confirm_button.setStyleSheet(self.stylesheet)

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

        # Populate tree view
        self.search_for_patient()

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

        self.dicom_file_controller.find_all_files()
        self.dicom_file_controller.find_DICOM_files()
        self.DICOM_files = self.dicom_file_controller.get_DICOM_files()
        self.display_files()

    def display_files(self):
        """
        Loop through dictionary of DICOM files and append these to the tree view.
        """
        for file in self.DICOM_files:
            temp_item = QTreeWidgetItem()
            name = ""
            if platform.system() == "Windows":
                name = file.split("\\")[-1]
            else:
                name = file.split("/")[-1]
            type = self.dicom_file_controller.get_type(self.DICOM_files[file])
            temp_item.setText(0, name)
            temp_item.setText(1, type)
            self.patient_tree.addTopLevelItem(temp_item)

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
        self.go_next_window.emit()
        self.window.close()

    def show(self):
        self.window.show()
