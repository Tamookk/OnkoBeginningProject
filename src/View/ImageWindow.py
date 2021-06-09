from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *
from Controller import ConfigurationRecordController, FindDICOMFileController
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np

class ImageWindow(QWidget):
    go_next_window = QtCore.Signal()
    go_previous_window = QtCore.Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Create window and layouts
        self.window = QWidget()
        self.window.setWindowTitle("Display Image")
        self.window.resize(1024, 1024)
        self.layout = QVBoxLayout()
        self.toolbar_layout = QGridLayout()
        self.patient_info_layout = QHBoxLayout()
        self.outside_tab_layout = QHBoxLayout()
        self.dicom_image_layout = QHBoxLayout()

        # Toolbar widgets
        self.placeholder_label = QLabel("Toolbar Placeholder")

        self.toolbar_layout.addWidget(self.placeholder_label)

        # Patient info widgets
        self.name_label = QLabel("Name: ")
        self.id_label = QLabel("ID: ")
        self.gender_label = QLabel("Gender: ")
        self.dob_label = QLabel("DoB: ")

        self.patient_info_layout.addWidget(self.name_label)
        self.patient_info_layout.addWidget(self.id_label)
        self.patient_info_layout.addWidget(self.gender_label)
        self.patient_info_layout.addWidget(self.dob_label)

        # Structures/isodoses tab widget
        self.struct_tabs = QTabWidget()
        self.structures_tab = QWidget()
        self.isodoses_tab = QWidget()
        self.struct_tabs.resize(600, 200)
        self.struct_tabs.addTab(self.structures_tab, "Structures")
        self.struct_tabs.addTab(self.isodoses_tab, "Isodoses")

        # DICOM view widgets
        self.dicom_tabs = QTabWidget()
        self.dicom_view_tab = QWidget()
        self.dvh_tab = QWidget()
        self.dicom_tree_tab = QWidget()
        self.clinical_data_tab = QWidget()
        self.dicom_tabs.addTab(self.dicom_view_tab, "DICOM View")
        self.dicom_tabs.addTab(self.dvh_tab, "DVH")
        self.dicom_tabs.addTab(self.dicom_tree_tab, "DICOM Tree")
        self.dicom_tabs.addTab(self.clinical_data_tab, "Clinical Data")

        # Image display widgets
        self.image_label = QLabel()
        self.slider = QSlider(QtCore.Qt.Vertical)

        # Load image for image label
        self.show_image()

        # DICOM View Layout
        temp_layout = QVBoxLayout()
        temp_layout.addWidget(self.image_label)
        self.dicom_image_layout.addLayout(temp_layout)
        self.dicom_image_layout.addWidget(self.slider)

        self.dicom_image_layout.addWidget(self.slider)

        self.dicom_view_tab.setLayout(self.dicom_image_layout)

        self.outside_tab_layout.addWidget(self.struct_tabs)
        self.outside_tab_layout.addWidget(self.dicom_tabs)

        # Add layouts to window
        self.layout.addLayout(self.toolbar_layout)
        self.layout.addLayout(self.patient_info_layout)
        self.layout.addLayout(self.outside_tab_layout)
        self.window.setLayout(self.layout)

    def get_image_data(self):
        """
        Gets image data from a DICOM file.
        """
        # Get DICOM file path
        configuration_record_controller = ConfigurationRecordController.ConfigurationRecordController()
        configuration_record_controller.connect_to_database()
        file_path = configuration_record_controller.get_default_directory()

        # Get a list of all DICOM files
        DICOM_file_controller = FindDICOMFileController.FindDICOMFileController(file_path)
        DICOM_file_controller.find_all_files()
        DICOM_file_controller.find_DICOM_files()
        DICOM_file_controller.check_elements()
        self.pixel_data = DICOM_file_controller.get_ct_image_data()

    def show_image(self):
        """
        Plots and shows image data gotten from DICOM file.
        """
        # Get DICOM file data
        self.get_image_data()

        # Update patient fields
        print(str(self.pixel_data['PatientName'].value))
        self.name_label.setText("Name: " + str(self.pixel_data['PatientName'].value))
        self.id_label.setText("ID: " + self.pixel_data['PatientID'].value)
        self.gender_label.setText("Gender: " + self.pixel_data['PatientSex'].value)
        self.dob_label.setText("DoB: " + self.pixel_data['PatientBirthDate'].value)

        # Try turn pixel data into image
        # from https://github.com/pydicom/contrib-pydicom/blob/master/viewers/pydicom_PIL.py
        ew = self.pixel_data['WindowWidth']
        ec = self.pixel_data['WindowCenter']
        ww = int(ew.value[0] if ew.VM > 1 else ew.value)
        wc = int(ec.value[0] if ec.VM > 1 else ec.value)
        data = self.pixel_data.pixel_array
        window = ww
        level = wc
        image = np.piecewise(data,
                     [data <= (level - 0.5 - (window - 1) / 2),
                      data > (level - 0.5 + (window - 1) / 2)],
                     [0, 255, lambda data: ((data - (level - 0.5)) /
                                            (window - 1) + 0.5) * (255 - 0)])
        im = Image.fromarray(image).convert('L')

        im = ImageQt(im)
        self.image_label.setPixmap(QPixmap.fromImage(im))

    def go_display_open_patient_window(self):
        """
        Go to previous window.
        """
        self.go_previous_window.emit()
        self.window.close()

    def show(self):
        self.window.show()
