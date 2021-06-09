from View import FirstTimeWindow, ImageWindow, OpenPatientWindow, WelcomeWindow
from PySide6 import QtWidgets


class Controller:
    def __init__(self):
        self.first_time_window = QtWidgets.QWidget()
        self.welcome_window = QtWidgets.QWidget()
        self.open_patient_window = QtWidgets.QWidget()
        self.image_window = QtWidgets.QWidget()

    def show_first_time(self):
        self.first_time_window = FirstTimeWindow.FirstTimeWindow()
        self.first_time_window.go_next_window.connect(self.show_open_patient)
        self.first_time_window.show()

    def show_welcome(self):
        self.welcome_window = WelcomeWindow.WelcomeWindow()
        self.welcome_window.go_next_window.connect(self.show_open_patient)
        self.welcome_window.show()

    def show_open_patient(self):
        self.open_patient_window = OpenPatientWindow.OpenPatientWindow()
        self.open_patient_window.go_next_window.connect(self.show_display_image)
        self.open_patient_window.go_previous_window.connect(self.show_welcome)
        self.open_patient_window.show()

    def show_display_image(self):
        self.image_window = ImageWindow.ImageWindow()
        self.image_window.go_previous_window.connect(self.show_open_patient)
        self.image_window.show()