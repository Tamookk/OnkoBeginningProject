from pydicom import dcmread
from pydicom.errors import InvalidDicomError
import numpy
import os.path


class FindDICOMFileController:
    def __init__(self, file_path):
        # Initialise variables
        self.file_path = file_path
        self.files = []
        self.DICOM_files = {}
        self.ct_image = numpy.empty([1, 1])

    def find_all_files(self):
        """
        Find all files in the default directory and sub-directories.
        """
        for root, dirs, files in os.walk(self.file_path, topdown=True):
            for name in files:
                self.files.append(os.path.join(root, name))

        if len(self.files) == 0:
            print("Error: no files found.")
        else:
            print("Found %s files." % len(self.files))

    def find_DICOM_files(self):
        """
        Find all DICOM files in the default directory.
        """
        count = 0
        if not len(self.files) == 0:
            for file in self.files:
                try:
                    dicom_file = dcmread(file)
                except (InvalidDicomError, FileNotFoundError):
                    pass
                else:
                    count += 1
                    self.DICOM_files[file] = dicom_file

        print("\nFound %s DICOM files." % len(self.DICOM_files))

    def get_DICOM_files(self):
        """
        Returns the list of DICOM files.
        :return: Dictionary of DICOM files found in self.file_path
        """
        return self.DICOM_files

    def get_ct_image_data(self):
        """
        Returns a numpy array of the pixel data of the first
        RT Image found when checking the directory (temporary, for
        initial sprint work).
        :return: self.ct_image, numpy array of pixel data
        """
        return self.ct_image

    def get_type(self, DICOM_file):
        """
        Returns the type of data contained within a DICOM file
        :return: type, string type of data in DICOM file
        """
        elements = {
            '1.2.840.10008.5.1.4.1.1.481.3': "RT Struct",
            '1.2.840.10008.5.1.4.1.1.2': "CT Image",
            '1.2.840.10008.5.1.4.1.1.481.2': "RT Dose",
            '1.2.840.10008.5.1.4.1.1.481.5': "RT Plan"
        }

        class_uid = DICOM_file["SOPClassUID"].value
        # Check to see what type of data the given DICOM file holds
        if class_uid in elements:
            return elements[class_uid]
        else:
            return "---"

    def check_elements(self):
        """
        Checks to see if the DICOM files have certain elements.
        :return: True if element exists.
        """
        # Return if there are no DICOM files
        if len(self.DICOM_files) == 0:
            print("Error: no DICOM files.")
            return

        # List of elements we are looking for (SOP Class UIDs and their meanings)
        elements = {
            '1.2.840.10008.5.1.4.1.1.481.3':    "RT Struct",
            '1.2.840.10008.5.1.4.1.1.2':        "CT Image",
            '1.2.840.10008.5.1.4.1.1.481.2':    "RT Dose",
            '1.2.840.10008.5.1.4.1.1.481.5':     "RT Plan"
        }

        # Dictionary of present elements
        elements_present = {
            "RT Struct": False, "CT Image": False,
             "RT Dose": False, "RT Plan": False
        }

        # Check each DICOM file to see what it contains
        for dicom_file in self.DICOM_files:
            class_uid = self.DICOM_files[dicom_file]["SOPClassUID"].value
            # Check to see if element is of interest and that we haven't already found it
            # in the DICOM file set
            if class_uid in elements:
                print("File %s contains %s" % (dicom_file, elements[class_uid]))
                if not elements_present[elements[class_uid]]:
                    if elements[class_uid] == "CT Image":
                        self.ct_image = self.DICOM_files[dicom_file]
                    elements_present[elements[class_uid]] = True

        # Print elements present in DICOM file
        print("DICOM Dataset contains:")
        print(elements_present)

        # Return true if DICOM Dataset contains > 0 elements
        return True in elements_present.values()

