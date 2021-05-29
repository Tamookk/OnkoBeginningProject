from pydicom import dcmread
from pydicom.errors import InvalidDicomError
import os.path


class FindDICOMFileController:
    def __init__(self, file_path):
        # Initialise variables
        self.file_path = file_path
        self.files = []
        self.DICOM_files = {}

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

        print("Found %s DICOM files." % len(self.DICOM_files))

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
                    elements_present[elements[class_uid]] = True

        # Print elements present in DICOM file
        print("DICOM Dataset contains:")
        print(elements_present)
