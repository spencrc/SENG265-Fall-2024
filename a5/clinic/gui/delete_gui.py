from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox

from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class DeleteGUI(QDialog):
    def __init__(self, controller, type_name, identifier, parent):
        super().__init__(parent)
        self.controller = controller
        self.type_name = type_name # Indicates whether type is Patient or Note
        self.identifier = identifier
        self.parent = parent

        self.setWindowTitle("Delete "+self.type_name) 

        layout = QVBoxLayout()
        
        self.label = QLabel(f"Are you sure you want to delete this {self.type_name}?")
        layout.addWidget(self.label)

        self.confirm_button = QPushButton("Yes")
        self.confirm_button.clicked.connect(self.delete)
        layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def delete(self):
        # Determines how to delete object depending on type
        if self.type_name == "Patient": 
            self.delete_patient()
        elif self.type_name == "Note":
            self.delete_note()

    def delete_patient(self):
        # Deletes Patient object 
        name = self.controller.search_patient(self.identifier).name
        try:
            self.controller.delete_patient(self.identifier)
            QMessageBox.information(self, "Success", f"Patient {name} deleted successfully.")
            self.accept()
        except (IllegalOperationException):
            QMessageBox.information(self, "Deletion Failure", f"Patient {name} could not be deleted! Please close their notes.")

    def delete_note(self):
        # Deletes Note object
        try:
            self.controller.delete_note(self.identifier)
            QMessageBox.information(self, "Success", f"Note {self.identifier} deleted successfully.")
            self.accept()
            self.parent.setEnabled(True)
        except (NoCurrentPatientException):
           QMessageBox.warning(self, "Deletion Failure", "Cannot delete note when there is no current patient!") 
           self.close()
