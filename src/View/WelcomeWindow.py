from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WelcomeWindow(QWidget):
    go_next_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Create window and layouts
        self.window = QWidget()
        self.window.setWindowTitle("Welcome Window")
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

        # Widgets
        self.logo = QPixmap("../assets/images/logo.png")
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo)
        self.welcome_text = """
                Customised welcome message.\t\t\t\t\t\n
                Or tips on how to use the software.\n
                Or traditional welcome message of OnkoDICOM.\n
                """
        self.welcome_text_label = QLabel(self.welcome_text)
        self.next_button = QPushButton("Next")

        # Add widgets to layout
        self.layout.addWidget(self.logo_label)
        self.layout.addWidget(self.welcome_text_label)
        self.layout.addWidget(self.next_button)

        # Attach functions to buttons
        self.next_button.clicked.connect(self.go_open_patient_window)

    def go_open_patient_window(self):
        """
        Go to the next window
        """
        self.go_next_window.emit()
        self.window.close()

    def show(self):
        self.window.show()
