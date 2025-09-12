from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Attendance System - Login")
        # self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: #f5f6fa;")
        self.setup_ui()

    def setup_ui(self):
        # Logo
        self.logo = QLabel(self)
        pixmap = QPixmap("fronted/logo.png") 
        self.logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)

        # Title
        self.title = QLabel("Welcome")
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #2f3640;")

        # Username and Password
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedHeight(40)
        self.username.setFont(QFont("Arial", 12))
        self.username.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dcdde1;
                border-radius: 10px;
                padding-left: 10px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #4cd137;
            }
        """)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(40)
        self.password.setFont(QFont("Arial", 12))
        self.password.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dcdde1;
                border-radius: 10px;
                padding-left: 10px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #4cd137;
            }
        """)

        # Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4cd137;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #44bd32;
            }
            QPushButton:pressed {
                background-color: #407a1d;
            }
        """)
        self.login_btn.setFixedHeight(40)

        # Layout
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.logo)
        vbox.addSpacing(10)
        vbox.addWidget(self.title)
        vbox.addSpacing(20)
        vbox.addWidget(self.username)
        vbox.addWidget(self.password)
        vbox.addSpacing(20)
        vbox.addWidget(self.login_btn)
        vbox.addStretch()
        vbox.setContentsMargins(50, 20, 50, 20)
        self.setLayout(vbox)
