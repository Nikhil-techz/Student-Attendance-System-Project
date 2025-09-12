import sys
import requests
from PyQt5.QtWidgets import QApplication
from .delete_ui import DeleteStudentUI

API_URL = "http://127.0.0.1:8000/students"

def delete_student(roll_no: str):
    """Function to delete student by roll_no"""
    try:
        response = requests.delete(f"{API_URL}/{roll_no}")  

        if response.status_code == 200:
            # Try parsing JSON safely
            try:
                data = response.json()
                return True, data.get("message", f"Student {roll_no} deleted successfully")
            except ValueError:
                return True, f"Student {roll_no} deleted successfully (no JSON in response)"

        elif response.status_code == 404:
            return False, f"Student with roll number {roll_no} not found."

        else:
            # Handle other error codes
            try:
                error = response.json().get("detail", f"Error deleting student {roll_no}")
            except ValueError:
                error = f"Error deleting student: Invalid response (status code {response.status_code})"
            return False, error

    except requests.RequestException as e:
        return False, f"Connection error: {str(e)}"
 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DeleteStudentUI(
        title="Delete Student Record",
        placeholder="Enter Roll Number",
        delete_func=delete_student
    )
    window.delete_button.clicked.connect(window.handle_delete) 
    window.show()

    sys.exit(app.exec_()) 
