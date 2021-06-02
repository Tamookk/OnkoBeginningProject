import unittest
import os, platform, sys, inspect
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from Controller.FindDICOMFileController import FindDICOMFileController


class TestDICOMFile(unittest.TestCase):
    """ This UnitTest checks that DICOM files from a specified directory are
        opened correctly in a fault-tolerant way, and finds all present
        elements in the DICOM file, regardless of what exists. """

    @classmethod
    def setUpClass(cls):
        print("Please enter the directory containing a DICOM Dataset: ")
        cls.test_directory = input()
        cls.controller = FindDICOMFileController(cls.test_directory)
        cls.controller.find_all_files()
        cls.controller.find_DICOM_files()

    def test_find_files(self):
        self.assertTrue(len(self.controller.files) > 0)

    def test_open_DICOM_files(self):
        self.assertTrue(len(self.controller.DICOM_files) > 0)

    def test_DICOM_contains_elements(self):
        self.assertTrue(self.controller.check_elements())


if __name__ == "__main__":
    unittest.main()