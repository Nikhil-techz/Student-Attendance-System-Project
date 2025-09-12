from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class StatusCard(QWidget):
    def __init__(self, title, value, color):
        super().__init__()
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: 12px;
            padding: 15px;
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")

        value_label = QLabel(str(value))
        value_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: white;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        self.setLayout(layout)
