from PyQt5.QtWidgets import QWidget , QLineEdit, QVBoxLayout, QComboBox,QPushButton,QMessageBox,QApplication
from .student_ui_style import CustomStyle
import sys
import requests
api_url = "http://127.0.0.1:8000/faculties/" 

class AddFaculty(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Faculty") 
        CustomStyle.apply(self)

        layout = QVBoxLayout() 

        self.faculty_name_input = QLineEdit()
        self.faculty_name_input.setPlaceholderText("Faculty Name")

        self.faculty_id_input = QLineEdit()
        self.faculty_id_input.setPlaceholderText("Faculty Id")

        self.faculty_phone_input = QLineEdit()
        self.faculty_phone_input.setPlaceholderText("Phone Number")

        self.faculty_depart_input = QLineEdit()
        self.faculty_depart_input.setPlaceholderText("Department")

        submit_btn = QPushButton("Add")
        submit_btn.clicked.connect(self.add_faculty)

        layout.addWidget(self.faculty_name_input)
        layout.addWidget(self.faculty_id_input)
        layout.addWidget(self.faculty_depart_input)
        layout.addWidget(self.faculty_phone_input) 
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def add_faculty(self):
        faculty_name = self.faculty_name_input.text().strip()
        faculty_id = self.faculty_id_input.text().strip().upper()
        department = self.faculty_depart_input.text().strip().upper()
        phone_no = self.faculty_phone_input.text().strip()

        if not faculty_name or not faculty_id or not department or not phone_no:
            QMessageBox.warning(self,"Input Error", "Please Fill all the Required Field.")
            return 
        
        try:
            response = requests.post(api_url,json={
                "name": faculty_name,
                "faculty_id":faculty_id,
                "department":department,
                "phone_no":phone_no

            })
            if response.status_code == 200:
                QMessageBox.information(self,"sucess","faculty details added successfully") 
                self.faculty_name_input.clear()
                self.faculty_id_input.clear()
                self.faculty_depart_input.clear()
                self.faculty_phone_input.clear()

            else:
                QMessageBox.critical(self,"Error",f"{response.text}")

            
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self,"Connection Error")

if __name__ == "__main__":
                               
    app = QApplication(sys.argv)
    window = AddFaculty() 
    window.show()
    sys.exit(app.exec_())   






    

        
        