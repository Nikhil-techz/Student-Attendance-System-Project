import sys
import requests
from PyQt5.QtWidgets import( QWidget, QLabel, QComboBox, QDateEdit, QPushButton, QVBoxLayout, 
QTableWidget, QTableWidgetItem, QMessageBox,QLineEdit,QApplication) 
from .student_ui_style import CustomStyle  

from PyQt5.QtCore import QDate

api_url = "http://127.0.0.1:8000/attendance/by-student/"
class ViewAttendance(QWidget):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("View Attendance")
        CustomStyle.apply(self) 
        self.init_ui()  

    def init_ui(self):
        layout = QVBoxLayout() 

        ##search the student by roll or name
        self.search_label = QLabel("Search by Name or Roll no")
        self.search_input = QLineEdit() 
        self.search_btn = QPushButton("search")
        self.search_btn.clicked.connect(self.search_attendance)  


        ##table for view data
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Roll no","Name","Subject","Faculty","Date","Status"])

        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def search_attendance(self):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self,"Error","Please Enter Name or Roll no")
            return 
        try:
            response = requests.get(f"http://127.0.0.1:8000/attendance/search?query={query}")
            if response.status_code== 200:
                records = response.json()
                self.table.setRowCount(len(records))
                for row,record  in enumerate(records):
                    self.table.setItem(row, 0, QTableWidgetItem(str(record.get("roll_no", ""))))
                    self.table.setItem(row, 1, QTableWidgetItem(record.get("name", "")))
                    self.table.setItem(row, 2, QTableWidgetItem(record.get("subject_name", "")))
                    self.table.setItem(row, 3, QTableWidgetItem(record.get("faculty_name", "")))
                    self.table.setItem(row, 4, QTableWidgetItem(record.get("date", "")))
                    self.table.setItem(row, 5, QTableWidgetItem(record.get("status", "")))


            else:
                    QMessageBox.warning(self,"Error","No record found") 

        except Exception as e:
            QMessageBox.critical(self,"Error",str(e)) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewAttendance()
    window.show()
    sys.exit(app.exec_())



        








       