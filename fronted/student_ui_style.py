from PyQt5.QtWidgets import QWidget

class CustomStyle:
    style = """
    QWidget {
        background-color:light sky;
        font-family: Arial;
        font-size: 14px;
    }

    QLineEdit {
        background-color: light pastel blue;
        padding: 6px;
        border: 1px solid lightgray;
        border-radius: 5px;
    }

    QLineEdit:focus {
        border: 1px solid dodgerblue;
        background-color: white;
    }

    QPushButton {
        background-color: blue;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color:green;
    }

    QComboBox {
        background-color:sky blue;
        padding: 6px;
        border-radius: 5px;
        border: 1px solid lightgray;
    }
    """

    @classmethod
    def apply(cls, widget: QWidget):
        """Apply the style to any QWidget or its children"""
        widget.setStyleSheet(cls.style)

