from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QVBoxLayout
import sys 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("student attendance system")
        layout = QVBoxLayout()

        buttons = {
            "Add Student": self.add_student,
            "Add Faculty": self.add_faculty,
            "Add Subject": self.add_subject,
            "Mark Attendance": self.mark_attendance,
            "View Attendance": self.view_attendance
        }

        for name ,func in buttons.items():
            btn = QPushButton(name)
            btn.clicked.connect(func)
            layout.addWidget(btn)

        self.setLayout(layout)


    def add_student(self):
        from add_student import AddStudent 
        self.window = AddStudent()
        self.window.show()


    def add_faculty(self):
        from add_faculty import AddFaculty
        self.window = AddFaculty()
        self.window.show()

    def add_subject(self):
        from add_subject import AddSubject
        self.window = AddSubject()
        self.window.show()

    def mark_attendance(self):
        from mark_attendance import MarkAttendance
        self.window = MarkAttendance()
        self.window.show()

    def view_attendance(self):
        from view_attendance import ViewAttendance
        self.window = ViewAttendance()
        self.window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.exit(app.exec())




