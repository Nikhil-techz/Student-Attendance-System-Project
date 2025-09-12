import sys
import requests
from PyQt5.QtWidgets import QApplication, QMessageBox
from .login_ui import LoginUI  
from .dashboard import Dashboard  

class LoginPage(LoginUI):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        
        self.login_btn.clicked.connect(self.login)

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return

        data = {"username": username, "password": password}

        try:
            res = requests.post("http://127.0.0.1:8000/auth/login", json=data)
            if res.status_code == 200:
                QMessageBox.information(self, "Success", "Login Successful")
                # Open Dashboard
                self.dashboard = Dashboard()
                self.dashboard.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid Credentials")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())  


    
