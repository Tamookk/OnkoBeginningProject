from Model import FirstTimeWindow, WelcomeWindow
from PyQt5 import QtWidgets


class Controller:
    def __init__(self):
        self.first_time_window = QtWidgets.QWidget()
        self.welcome_window = QtWidgets.QWidget()

    def show_first_time(self):
        self.first_time_window = FirstTimeWindow.FirstTimeWindow()
        self.first_time_window.go_next_window.connect(self.show_open_patient)
        self.first_time_window.show()

    def show_welcome(self):
        self.welcome_window = WelcomeWindow.WelcomeWindow()
        self.welcome_window.go_next_window.connect(self.show_open_patient)
        self.welcome_window.show()

    def show_open_patient(self):
        print("Next window...")