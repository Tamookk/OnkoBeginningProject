import os
import platform


class DirectoryManager:

    def __init__(self):
        pass

    @staticmethod
    def determine_correct_path(directory_name):
        """
        Linux, Windows and OSX
        Determine the path for the default directory
        This directory is to be hidden directory in the users home directory
        """

        desired_path = ""

        if platform.system() == "Windows":
            desired_path = "\\.OnkoDICOM\\"
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            desired_path = "/.OnkoDICOM/"
        else:
            print("System not recognised. \nOnkoDICOM only supported on Linux, Windows & OS X systems.")
            exit()

        return directory_name + desired_path

    @staticmethod
    def windows_make_directory_hidden(directory):
        """ Windows only -- Additional step needed to make directory hidden """

        os.system("attrib +h " + directory[:-1])

    @staticmethod
    def remove_directory(directory_name):
        """ Check that the path exists, then remove it """

        if os.path.exists(directory_name):
            os.rmdir(directory_name)
            print("Removed the path '%s'" % directory_name)
        else:
            print ("Path '%s' not found" % directory_name)

    @staticmethod
    def create_directory(directory):
        """ If the directory already exists, tell the user
            Otherwise, create the path """

        if os.path.exists(directory):
            print("The path '%s' directory already exists" % directory)
        else:
            try:
                os.mkdir(directory)
                if platform.system() == "Windows":
                    DirectoryManager.windows_make_directory_hidden(directory)
                if os.path.exists(directory):
                    print("Successfully created directory '%s'" % directory)
                else:
                    print("An error occurred: Could not create directory '%s'" % directory)
            except:
                print("An error occurred: Could not create directory '%s'" % directory)


if __name__ == "__main__":
    """ Determine the correct path to place hidden directory, in this case '.OnkoDICOM' """
    hidden_path = DirectoryManager.determine_correct_path(".OnkoDICOM")

    """ Create the path using the hidden_path we determined previously"""
    DirectoryManager.create_directory(hidden_path)

    """ Remove the path we just created """
    # DirectoryManager.remove_directory(hidden_path)