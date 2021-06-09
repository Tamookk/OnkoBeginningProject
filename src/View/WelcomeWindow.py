from PyQt5 import QtCore
from PyQt5 import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WelcomeWindow(QWidget):
    go_next_window = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Create window and layouts
        self.window = QWidget()
        self.window.setWindowTitle("Onko Beginning Project")
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)
        self.window.resize(840, 530)
        self.layout.setAlignment(Qt.Qt.AlignCenter)

        # Widgets
        self.logo_holder = QHBoxLayout()
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("../assets/images/logo.png"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(480, 260)
        self.logo_holder.addStretch(1)
        self.logo_holder.addWidget(self.logo_label)
        self.logo_holder.addStretch(1)

        self.welcome_text = "Welcome to Onko Beginning Project!"
        self.description_text = "OnkoDICOM - the solution for producing data for analysis from your oncology plans and scans"
        self.welcome_font = QFont()
        self.welcome_font.setBold(True)
        self.welcome_font.setPointSize(18)
        self.description_font = QFont()
        self.description_font.setWeight(0.5)
        self.description_font.setPixelSize(16)

        self.welcome_text_label = QLabel(self.welcome_text)
        self.welcome_text_label.setAlignment(Qt.Qt.AlignCenter)
        self.description_text_label = QLabel(self.description_text)
        self.description_text_label.setAlignment(Qt.Qt.AlignCenter)

        self.welcome_text_label.setFont(self.welcome_font)
        self.description_text_label.setFont(self.description_font)

        self.button_stylesheet = """
        QPushButton
        {
            margin: 4px;
            padding: 0 16px;
            min-height: 36px;
            border-radius: 2px;
            color: #f5f5f5;
            background-color: #9370DB;
            font-family: "Segoe UI", "Roboto", "Helvetica Neue", sans-serif;
            font-size: 14px;
            text-align: center;
            qproperty-iconSize: 18px;
        }
        QPushButton:hover
        {   
            /* +10% saturation */
            background-color: #b299e6;
        }
        QPushButton:pressed
        {
            /* -20% saturation */
            background-color: #5c2eb8;
        }"""

        self.next_button = QPushButton("Next")
        self.next_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.next_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.next_button.resize(480, 261)
        self.next_button.setStyleSheet(self.button_stylesheet)
        self.buttons_holder = QHBoxLayout()
        self.buttons_holder.addStretch(1)
        self.buttons_holder.addWidget(self.next_button)
        self.buttons_holder.addStretch(1)

        # Add widgets to layout
        self.layout.addLayout(self.logo_holder)
        self.layout.addWidget(self.welcome_text_label)
        self.layout.addWidget(self.description_text_label)
        self.layout.addSpacing(30)
        self.layout.addLayout(self.buttons_holder)

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
