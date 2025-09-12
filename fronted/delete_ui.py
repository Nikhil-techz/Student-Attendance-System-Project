from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class DeleteStudentUI(QWidget):
    def __init__(self, title="Delete Student", placeholder="Enter Roll Number", delete_func=None):
        super().__init__()
        self.delete_func = delete_func
        self.setWindowTitle(title)
        self.setGeometry(500, 200, 400, 220)
        self.setStyleSheet("background-color: #f4f6f9;")  # Window background
        self.init_ui(placeholder)  

    def init_ui(self, placeholder):
        # Label
        self.label = QLabel("Enter Roll Number:", self)
        self.label.setFont(QFont("Arial", 13, QFont.Bold))
        self.label.setStyleSheet("color: dark navy-grey;")  # Dark navy-grey
        self.label.setAlignment(Qt.AlignCenter)  

        # Input
        self.roll_input = QLineEdit(self)
        self.roll_input.setPlaceholderText(placeholder)
        self.roll_input.setFont(QFont("Arial", 11))
        self.roll_input.setFixedHeight(35)
        self.roll_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid bright blue;
                border-radius: 8px;
                padding: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid dark blue;
                background-color: alice blue tint;
            }
        """)

        # Delete Button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setFixedHeight(40)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: lavender mist;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color:Dodger blue;
            }
        """) 

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.label)
        layout.addWidget(self.roll_input)
        layout.addWidget(self.delete_button)
        self.setLayout(layout)

    def handle_delete(self):
        roll_no = self.roll_input.text().strip()
        if not roll_no:
            QMessageBox.warning(self, "Input Error", "Please enter a roll number.")
            return

        if self.delete_func:
            success, msg = self.delete_func(roll_no)
            if success:
                QMessageBox.information(self, "Success", msg)
            else:
                QMessageBox.critical(self, "Error", msg)
