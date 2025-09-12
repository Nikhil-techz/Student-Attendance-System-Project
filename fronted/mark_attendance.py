import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, QDateEdit,QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QDate, QThread, pyqtSignal, QTimer
from .student_ui_style import CustomStyle  

api_url = "http://127.0.0.1:8000/attendance/"

class Student:
    def __init__(self, roll_no, name,batch,gender=None,id=None):
        self.roll_no = roll_no
        self.name = name
        self.batch = batch
        self.gender =gender 
        self.id = id

class Subject:
    def __init__(self, subj_id, subject_name, faculty_id):
        self.subj_id = subj_id
        self.subject_name = subject_name
        self.faculty_id = faculty_id 


# ---- worker class ----
class ApiFetcher(QThread):
    data_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, url, mode, params=None):
        """
        url: API endpoint to fetch
        mode: 'students' or 'subjects' 
        """
        super().__init__()
        self.url = url
        self.mode = mode
        self.params = params 

    def run(self):
        """Run in background thread"""
        try:
            response = requests.get(self.url, params=self.params) 
            if response.status_code == 200:
                self.data_loaded.emit(response.json())
            else:
                self.error_occurred.emit(
                    f"Failed to load {self.mode} (status {response.status_code})"
                )
        except Exception as e:
            self.error_occurred.emit(f"Error loading {self.mode}: {str(e)}")


# ------ Main UI ------
class MarkAttendance(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mark Attendance")  
        CustomStyle.apply(self) 
        self.subjects = []
        self.students = []
        self.init_ui()

        # load data after UI is ready
        QTimer.singleShot(0, self.load_students)
        QTimer.singleShot(0, self.load_subjects) 

    def init_ui(self):
        layout = QVBoxLayout()

        # student
        self.student_label = QLabel("Select Student:")
        self.student_combo = QComboBox()
        self.student_combo.addItem("select student", None) 

        # subject
        self.subject_label = QLabel("Select Subject:")
        self.subject_input = QComboBox()
        self.subject_input.addItem("select subject", None)

        # date
        self.date_label = QLabel("Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        today = QDate.currentDate()
        self.date_input.setDate(today)
        self.date_input.setMinimumDate(today.addDays(-7)) 
        self.date_input.setMaximumDate(today)


        

        # attendance
        self.status_label = QLabel("Attendance Status:")
        self.status_input = QComboBox()
        self.status_input.addItem("select status", None)
        self.status_input.addItems(["Present", "Absent"]) 

        # button
        self.submit_btn = QPushButton("Mark Attendance")
        self.submit_btn.clicked.connect(self.mark_attendance)

        # add widgets to layout
        layout.addWidget(self.student_label)
        layout.addWidget(self.student_combo)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    # ---- Load Students -------
    def load_students(self):
        self.student_thread = ApiFetcher("http://127.0.0.1:8000/students", "students")
        self.student_thread.data_loaded.connect(self.populate_students)
        self.student_thread.error_occurred.connect(self.show_error) 
        self.student_thread.start()

    def populate_students(self, students):
        
        self.student_combo.clear()
        self.student_combo.addItem("select student", None)
        self.students = [Student(**s) for s in students] 
        for student in self.students:
            display_text = f"{student.name} -({student.roll_no})"
            self.student_combo.addItem(display_text, student.roll_no) 

    # ------ Load Subjects ------
    def load_subjects(self, subject_id=None): 
        
        params = {"subject_id": subject_id} if subject_id else None
        self.subject_thread = ApiFetcher("http://127.0.0.1:8000/subjects", "subjects", params=params)
        self.subject_thread.data_loaded.connect(self.populate_subjects)
        self.subject_thread.error_occurred.connect(self.show_error)
        self.subject_thread.start()  

    def populate_subjects(self, subjects):
       self.subjects = [Subject(**s) for s in subjects] 
       self.subject_input.clear()
       self.subject_input.addItem("select subject", None)
       for subject in self.subjects:
            display_text = f"{subject.subject_name}-({subject.faculty_id})" 
            self.subject_input.addItem(display_text, subject.subj_id)      

    # --- Error Handling -------
    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)

    # -- Submit Attendance -----
    def mark_attendance(self):
        roll_no = self.student_combo.currentData()
        subject_id = self.subject_input.currentData()
        date = self.date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText()  

        if roll_no is None: 
            QMessageBox.warning(self, "Error", "Please select a student.")
            return
        if subject_id is None:
            QMessageBox.warning(self, "Error", "Please select a subject.")
            return
        if self.status_input.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Please select attendance status.")
            return

        data = {
            "roll_no": roll_no,
            "subject_id": subject_id, 
            "date": date,
            "status": status 
        }

        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Attendance marked successfully!")

                self.student_combo.setCurrentIndex(0)
                self.subject_input.setCurrentIndex(0)
                self.status_input.setCurrentIndex(0)
                 
            else:
                QMessageBox.warning(
                    self, "Error",
                    f"Failed: {response.json().get('detail', 'Unknown error')}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


#---- Run App ----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkAttendance()
    window.show()
    sys.exit(app.exec_())  
