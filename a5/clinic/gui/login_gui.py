from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout

from clinic.exception.invalid_login_exception import InvalidLoginException

class LoginGUI(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("User Login")

        layout = QGridLayout()

        label_username = QLabel("Username")
        self.text_username = QLineEdit()
        label_password = QLabel("Password")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button_login = QPushButton("Login")
        self.button_quit = QPushButton("Quit")

        layout.addWidget(label_username, 0, 0)
        layout.addWidget(self.text_username, 0, 1)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.text_password, 1, 1)
        layout.addWidget(self.button_login, 2, 0)
        layout.addWidget(self.button_quit, 2, 1)
        self.setLayout(layout)

        # connect the buttons' clicked signals to the slots below
        self.button_login.clicked.connect(self.login_button_clicked)
        self.button_quit.clicked.connect(self.reject)
    
    def login_button_clicked(self):
        username = self.text_username.text()
        password = self.text_password.text()

        try:
            self.controller.login(username, password) #passes username and password to controller to attempt login
            self.accept() #if login successful, user goes to main menu
        except InvalidLoginException:
            QMessageBox.warning(self, "Invalid Login", "Incorrect username or password!")

        self.text_username.setText("") #resets input box so the user can retry
        self.text_password.setText("") #resets input box so the user can retry