from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator

from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class CreateEditGui(QWidget):
    def __init__(self, parent, type_name, selected_object=None):
        super().__init__()
        self.parent = parent
        self.controller = self.parent.controller
        self.type_name = type_name # Indicates whether type is Patient or Note
        self.selected_object = selected_object #passing patient as a parameter implies we are editing, OTHERWISE creating
        self.layout = QVBoxLayout()

        # Disables parent window when child window is open
        self.parent.setEnabled(False)

        # Initialize the GUI based on the type_name
        if self.type_name == "Patient":
            self.init_for_patient()
        elif self.type_name == "Note":
            self.init_for_note()
        else:
            print("There was an invalid arg passed to CreateEditGUI! It was: "+type_name)
            return
        
        # Populate fields if editing an existing object
        if self.selected_object:
            if self.type_name == "Patient":
                self.text_phn.setText(str(self.selected_object.phn))
                self.text_name.setText(self.selected_object.name)
                self.text_dob.setText(self.selected_object.birth_date)
                self.text_phone.setText(self.selected_object.phone)
                self.text_email.setText(self.selected_object.email)
                self.text_address.setText(self.selected_object.address)
            elif self.type_name == "Note":
                self.text_contents.setText(str(self.selected_object.text))
            self.setWindowTitle("Update "+self.type_name)
        else:
            self.setWindowTitle("Create "+self.type_name)

        layout2 = QHBoxLayout()

        self.button_clear = QPushButton("Clear")
        self.button_complete = QPushButton("Complete")
        self.button_cancel = QPushButton("Cancel")
        layout2.addWidget(self.button_complete)
        layout2.addWidget(self.button_clear)
        self.layout.addLayout(layout2)

        self.setLayout(self.layout)

        self.button_clear.clicked.connect(self.clear)
        self.button_complete.clicked.connect(self.complete)
        #self.button_cancel.clicked.connect(self.close)

    def init_for_patient(self):
        # Initializes the GUI for creating/editing a Patient
        layout1 = QGridLayout()

        label_phn = QLabel("PHN")
        label_name = QLabel("Full Name")
        label_dob = QLabel("Birthdate")
        label_phone = QLabel("Phone Number")
        label_email = QLabel("Email")
        label_address = QLabel("Address")
        int_validator = QIntValidator()
        self.text_phn = QLineEdit()
        self.text_phn.setValidator(int_validator)
        self.text_name = QLineEdit()
        self.text_dob = QLineEdit()
        self.text_phone = QLineEdit()
        self.text_email = QLineEdit()
        self.text_address = QLineEdit()

        layout1.addWidget(label_phn, 0, 0)
        layout1.addWidget(self.text_phn, 0, 1)
        layout1.addWidget(label_name, 1, 0)
        layout1.addWidget(self.text_name, 1, 1)
        layout1.addWidget(label_dob, 2, 0)
        layout1.addWidget(self.text_dob, 2, 1)
        layout1.addWidget(label_phone, 3, 0)
        layout1.addWidget(self.text_phone, 3, 1)
        layout1.addWidget(label_email, 4, 0)
        layout1.addWidget(self.text_email, 4, 1)
        layout1.addWidget(label_address, 5, 0)
        layout1.addWidget(self.text_address, 5, 1)
        self.layout.addLayout(layout1)

    def init_for_note(self):
        # Initializes the GUI for creating/editing a Note
        layout1 = QHBoxLayout()

        label_text = QLabel("Text")
        self.text_contents = QLineEdit()

        layout1.addWidget(label_text)
        layout1.addWidget(self.text_contents)

        self.layout.addLayout(layout1)

    def clear(self):
        # Clears all input fields
        if self.type_name == "Patient":
            self.text_phn.clear()
            self.text_name.clear()
            self.text_dob.clear()
            self.text_phone.clear()
            self.text_email.clear()
            self.text_address.clear()
        elif self.type_name == "Note":
            self.text_contents.clear()

    def complete(self):
        # Completes the creation or editing process
        if self.type_name == "Patient":
            if self.selected_object: #editing patient
                self.update_patient()
            else:
                self.create_patient()
        elif self.type_name == "Note":
            if self.selected_object: #editing note
                self.update_note()
            else:
                self.create_note()

    def update_patient(self):
        # Updates an existing patient's information
        phn2 = int(self.text_phn.text())
        name = str(self.text_name.text())
        dob = str(self.text_dob.text())
        phone = str(self.text_phone.text())
        email = str(self.text_email.text())
        address = str(self.text_address.text())
        try:
            self.controller.update_patient(self.selected_object.phn, phn2, name, dob, phone, email, address)
            QMessageBox.information(self, "Update Successful", f"Patient {name} was successfully updated!")
            self.parent.patient_model.redo_refresh()
            self.close()
        except (IllegalOperationException):
            QMessageBox.warning(self, "Update Failure", f"Something went wrong! Were you trying to edit the current patient or set Patient {self.selected_object.name}'s PHN to another patient's PHN?")

    def create_patient(self):
        # Creates a new patient
        phn = int(self.text_phn.text())
        name = str(self.text_name.text())
        dob = str(self.text_dob.text())
        phone = str(self.text_phone.text())
        email = str(self.text_email.text())
        address = str(self.text_address.text())
        try:
            self.controller.create_patient(phn, name, dob, phone, email, address)
            QMessageBox.information(self, "Patient Created", f"Patient {name} was successfully registered!")
            self.parent.patient_model.redo_refresh()
            self.close()
        except (IllegalOperationException):
            QMessageBox.warning(self, "Creation Failure", "Cannot create a patient using a PHN registered to another patient!")

    def update_note(self):
        # Updates text contents of existing note
        text = str(self.text_contents.text())
        try:
            self.controller.update_note(self.selected_object.code, text)
            QMessageBox.information(self, "Update Successful", f"Note {self.selected_object.code} was successfully updated!")
            self.parent.redo_refresh()
            self.close()
        except (NoCurrentPatientException):
            QMessageBox.warning(self, "Update Failure", "Cannot update note when there is no current patient!") 
            self.close()

    def create_note(self):
        # Creates a new note
        text = str(self.text_contents.text())
        try:
            new_note = self.controller.create_note(text)
            QMessageBox.information(self, "Note Created", f"Note {new_note.code} was successfully created!")
            self.parent.redo_refresh()
            self.close()
        except (NoCurrentPatientException):
           QMessageBox.warning(self, "Creation Failure", "Cannot create note when there is no current patient!") 
           self.close()

    def closeEvent(self, event):
        self.parent.setEnabled(True)