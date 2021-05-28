from pydicom import dcmread
from pydicom.errors import InvalidDicomError
import os.path


class FindDICOMFileController:
    def __init__(self, file_path):
        # Initialise variables
        self.file_path = file_path
        self.files = []
        self.DICOM_files = []

    def find_all_files(self):
        """
        Find all files in the default directory.
        """
        for root, dirs, files in os.walk(self.file_path, topdown=True):
            for name in files:
                self.files.append(os.path.join(root, name))
            for name in dirs:
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
                except:
                    pass
                else:
                    count += 1
                    self.DICOM_files.append(file)

        print("Found %s DICOM files." % len(self.DICOM_files))