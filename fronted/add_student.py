from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QMessageBox,QApplication

from  .student_ui_style import CustomStyle  
import requests
import sys

api_url = "http://127.0.0.1:8000/students/" 

class AddStudent(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Add Student") 
        CustomStyle.apply(self) 

        layout = QVBoxLayout()

        self.all_genders = ["Male","Female"] 
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.roll_input = QLineEdit()
        self.roll_input.setPlaceholderText("Roll No")


        self.batch_input = QLineEdit()
        self.batch_input.setPlaceholderText("Batch")

        ## dropdown for gender input. 
        self.gender_input = QComboBox()
        self.gender_input.addItem("select Gender")
        self.gender_input.addItems(self.all_genders)
        self.gender_input.setCurrentIndex(0)  
        

        submit_btn = QPushButton("Add")
        submit_btn.clicked.connect(self.add_student)

        layout.addWidget(self.name_input)
        layout.addWidget(self.roll_input)
        layout.addWidget(self.batch_input)
        layout.addWidget(self.gender_input)
        layout.addWidget(submit_btn)

        self.setLayout(layout)



    def add_student(self):
        name = self.name_input.text().strip()
        roll_no = self.roll_input.text().strip().upper()
        batch = self.batch_input.text().strip().upper() 
        gender = self.gender_input.currentText()

        if not name or not roll_no or not batch:
            QMessageBox.warning(self, "Input Error", "Please fill all the required fields.")
            return
     

        try:
            response = requests.post(api_url,json = {
                "name": name,
                "roll_no":roll_no,
                "batch":batch,
                "gender": gender

            })
            if response.status_code == 200:
                QMessageBox.information(self,"success","student added successfully.")
                self.name_input.clear() 
                self.roll_input.clear()
                self.batch_input.clear()
                self.gender_input.setCurrentIndex(0)    

            else:
                QMessageBox.critical(self,"Error",f"{response.text}") 


        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self,"Connection Eroor")


if __name__ == "__main__":
    
    app = QApplication(sys.argv) 
    window = AddStudent()
    window.show()
    sys.exit(app.exec_())


        






    
