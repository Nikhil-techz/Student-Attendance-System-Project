from PyQt5.QtWidgets import QWidget , QLineEdit, QVBoxLayout,QLabel, QComboBox,QPushButton,QMessageBox,QApplication
from .student_ui_style import CustomStyle
import sys
import requests

api_url = "http://127.0.0.1:8000/subjects/"  

class AddSubject(QWidget):
    def __init__(self):                            
        super().__init__()
        self.setWindowTitle("Add Subjects")
        CustomStyle.apply(self)

        layout = QVBoxLayout() 

        ##lables  and inputs for subject id

        self.subject_id_label = QLabel("Subject ID")
        self.subject_id_input = QLineEdit()
        self.subject_id_input.setPlaceholderText("Enter Subject ID")

        ## labels and input for subject name
        self.subject_name_label = QLabel("Subject Name")
        self.subject_name_input = QLineEdit()
        self.subject_name_input.setPlaceholderText("Enter Subject Name")
        
         ##labels and input for faculty id
        self.faculty_id_label = QLabel("Faculty ID") 
        self.faculty_id_input = QLineEdit() 
        self.faculty_id_input.setPlaceholderText("Enter Faculty ID Of Suject Teacher") 

        ## submit buttton
        self.submit_btn = QPushButton("Add Subject")
        self.submit_btn.clicked.connect(self.add_subject)

        #add widget to layout
        layout.addWidget(self.subject_id_label)
        layout.addWidget(self.subject_id_input)
        layout.addWidget(self.subject_name_label)
        layout.addWidget(self.subject_name_input)
        layout.addWidget(self.faculty_id_label)
        layout.addWidget(self.faculty_id_input)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout) 

    def add_subject(self):
        subject_id= self.subject_id_input.text()
        subject_name=self.subject_name_input.text()
        faculty_id=self.faculty_id_input.text()

        if not subject_id or not subject_name or not faculty_id:
            QMessageBox.warning(self,"please fill all the fields")
            return 
        
        try:
            response = requests.post(api_url,json={ 
                "subj_id":subject_id,
                 "subject_name":subject_name, 
                 "faculty_id":faculty_id  
            })  
            if response.status_code in (200,201): 
                QMessageBox.information(self,"sucess","Subjects Details Added Successfully.") 
                self.subject_id_input.clear()
                self.subject_name_input.clear()
                self.faculty_id_input.clear()


            else:
                QMessageBox.critical(self,"Error",f"{response.text}")

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self,"Connection Error")

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddSubject()
    window.show()
    sys.exit(app.exec_()) 

        
