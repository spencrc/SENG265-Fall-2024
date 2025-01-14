from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout

class SearchPatientGUI(QWidget):
    def __init__(self, controller, parent):
        super().__init__()
        self.controller = controller
        self.parent = parent
        self.setWindowTitle("Search for Patient")

        layout = QGridLayout()

        label_phn = QLabel("Enter Patient PHN or Name:")
        self.text_phn = QLineEdit()
        
        layout.addWidget(label_phn, 0, 0)
        layout.addWidget(self.text_phn, 0, 1)
        self.button_search = QPushButton("Search")
        layout.addWidget(self.button_search, 1, 0)
        self.button_cancel = QPushButton("Cancel")
        layout.addWidget(self.button_cancel, 1, 1)
        self.setLayout(layout)

        # defining widgets initial state
        self.text_phn.setEnabled(True)
        self.button_search.setEnabled(True)
        self.button_cancel.setEnabled(True)

        # handle text change to enable/disable the create button
        self.text_phn.textChanged.connect(self.patient_text_changed)

        # connect the buttons' clicked signals to the slots below
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_cancel.clicked.connect(self.close)

    def patient_text_changed(self):
        # Enable or disable Search button depending on whether or not there is text input
        if self.text_phn.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

    def search_button_clicked(self):
        # Searches for Patient either by phn or name
        search_input = self.text_phn.text()
        try: # See if input was an integer
            phn = int(search_input)
            patient = self.controller.search_patient(phn)
            if patient:
                QMessageBox.information(self, "Search Successful", f"Patient {patient.name} found!")
                self.parent.patient_model.refresh_via_search(phn)
                self.close()
            else:
                QMessageBox.warning(self, "Search Failure", "Patient not found!")
            
        except (ValueError): # If the input was not an integer, go here
            patient_list = self.controller.retrieve_patients(search_input)
            if patient_list:
                QMessageBox.information(self, "Search Successful", "Patients found!")
                self.parent.patient_model.refresh_via_retrieve(search_input)
                self.close()
            else:
                QMessageBox.warning(self, "Search Failure", "Patients not found!")

    def closeEvent(self, event):
        self.parent.setEnabled(True)
        