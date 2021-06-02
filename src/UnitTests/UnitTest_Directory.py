import unittest
import os, sys
from os.path import expanduser
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from DirectoryManager import DirectoryManager


def get_home_directory():
    # Set home directory
    return expanduser("~")


def create_directory(directory_name):
    """ Determine the correct path to place hidden directory, in this case '.OnkoDICOM' """
    hidden_dir = DirectoryManager.determine_correct_path(directory_name)

    """ Create the path using the hidden_path we determined previously"""
    DirectoryManager.create_directory(hidden_dir)


def remove_directory(directory_name):
    """ Remove the path we just created """
    DirectoryManager.remove_directory(directory_name)


class TestHome(unittest.TestCase):
    # Test if home directory found actually exists
    def testHome(self):
        home_dir = get_home_directory()
        self.assertTrue(os.path.exists(home_dir))


class TestCreate(unittest.TestCase):
    # Check if a hidden directory is created
    def testCreate(self):
        home_dir = get_home_directory()
        dir_name = ".OnkoDICOM"
        create_directory(dir_name)
        self.assertTrue(os.path.exists(home_dir + '\\' + dir_name))


class TestDelete(unittest.TestCase):
    # Check that the deleted directly no longer exists
    def testDelete(self):
        home_dir = get_home_directory()
        dir_name = ".OnkoDICOM"
        remove_directory(DirectoryManager.determine_correct_path(dir_name))
        self.assertFalse(os.path.exists(home_dir + '\\' + dir_name))


unittest.main(argv=[''], verbosity=2, exit=False)
