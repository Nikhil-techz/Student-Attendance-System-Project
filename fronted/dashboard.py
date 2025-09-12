import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFrame,QHBoxLayout, QPushButton,QVBoxLayout,QWidget,QLabel, QGridLayout,QInputDialog,QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QDateTime,QTimer
from .add_student import AddStudent
from .add_faculty import AddFaculty
from .add_subject import AddSubject
from .mark_attendance import MarkAttendance
from .view_attendance import ViewAttendance 
from .delete_student import delete_student
from .stats import get_total_student, get_total_faculty, get_total_subject, get_present_today
from .status_card import StatusCard 


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Attendance - Dashboard")
        self.setGeometry(300,150,500,500)
        self.setStyleSheet("background-color: light grey")

        layout= QVBoxLayout() 
        layout.setSpacing(15)
         
         ##header ##

        header = QFrame()
        header.setStyleSheet("background-color: #34495e; color: white;")
        header.setFixedHeight(60)
        header_layout = QHBoxLayout()

        title = QLabel("Student Attendance Dashboard")
        title.setFont(QFont("Segoe UI",18,QFont.Bold))
        title.setStyleSheet("color:white;") 

        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont("Segoe UI", 12))
        self.datetime_label.setStyleSheet("color: white;")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.datetime_label)
        header.setLayout(header_layout)
        layout.addWidget(header)
         
         ##  --timer to update time  ## --- 
        timer = QTimer(self) 
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time() 


        stats_layout = QGridLayout()
        stats_layout.setSpacing(20) 

        self.total_students_card = StatusCard("Total Students", get_total_student(),  "MediumSlateBlue")
        self.present_today_card = StatusCard("Present Today", get_present_today(),  "MediumSeaGreen")
        self.total_faculty_card = StatusCard("Total Faculty", get_total_faculty(),  "DarkOrange")
        self.total_subjects_card = StatusCard("Total Subjects", get_total_subject(),  "LightSeaGreen")

        stats_layout.addWidget(self.total_students_card, 0, 0)
        stats_layout.addWidget(self.present_today_card, 0, 1)
        stats_layout.addWidget(self.total_faculty_card, 1, 0)
        stats_layout.addWidget(self.total_subjects_card, 1, 1)
        
        layout.addLayout(stats_layout)  



        ##buttons ---  ## 
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignHCenter)   

        self.btn_add_student = self.create_button("Add student", self.open_add_student)
        self.btn_delete_student = self.create_button("Delete student",self.open_delete_student)
        self.btn_add_faculty = self.create_button("Add faculty",self.open_add_faculty)
          
        self.btn_add_subject = self.create_button("Add subject",self.open_add_subject)
        self.btn_mark_attendance = self.create_button("Mark Attendance",self.open_mark_attendance)
        self.btn_view_attendance = self.create_button("View Attendance",self.open_view_attendance)

        btn_layout.addWidget(self.btn_add_student)
        btn_layout.addWidget(self.btn_delete_student)
        btn_layout.addWidget(self.btn_add_faculty)
        btn_layout.addWidget(self.btn_add_subject)
        btn_layout.addWidget(self.btn_mark_attendance)
        btn_layout.addWidget(self.btn_view_attendance) 

        layout.addLayout(btn_layout)
 
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def create_button(self, text, slot):
        """function to create styled buttons"""
        button = QPushButton(text)
        button.setFont(QFont("Segoe UI", 12))
        button.setFixedSize(155,45)
        button.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: lightgrey;
            }
            QPushButton:pressed {
                background-color: grey;
            }
        """)
        button.clicked.connect(slot)
        return button
    
    ##window open 

    def open_add_student(self): 
        self.student_window = AddStudent()
        self.student_window.show()

    def open_delete_student(self):
        roll_no, ok = QInputDialog.getText(self,"Delete student","Enter Roll Number:")
        if ok and roll_no:
            delete_student(roll_no)
            QMessageBox.information(self,"Deleted",f"student with {roll_no} deleted sucessfully")

    def open_add_faculty(self):
        self.faculty_window = AddFaculty()
        self.faculty_window.show()

    def open_add_subject(self):
        self.subject_window = AddSubject()
        self.subject_window.show()

    def open_mark_attendance(self):
        self.markattendance_window = MarkAttendance()
        self.markattendance_window.show()

    def open_view_attendance(self):
        self.viewattendance_window = ViewAttendance()
        self.viewattendance_window.show()

## date / time update ##  
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss")
        self.datetime_label.setText(current_time)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())  











