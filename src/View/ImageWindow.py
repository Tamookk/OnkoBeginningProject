from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from Controller import ConfigurationRecordController, FindDICOMFileController
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np

class ImageWindow(QWidget):
    go_next_window = QtCore.pyqtSignal()
    go_previous_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Create window and layout
        self.window = QWidget()
        self.window.setWindowTitle("Image Window")
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

        # Widgets
        self.image_label = QLabel()
        self.back_button = QPushButton("Back")
        self.image_button = QPushButton("Show Image")

        # Add widgets to layout
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.back_button)
        self.layout.addWidget(self.image_button)

        # Connect buttons to functions
        self.back_button.clicked.connect(self.go_display_open_patient_window)
        self.image_button.clicked.connect(self.show_image)

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
