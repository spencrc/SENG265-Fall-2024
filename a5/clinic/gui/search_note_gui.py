from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout

from clinic.gui.create_edit_gui import CreateEditGui
from clinic.gui.delete_gui import DeleteGUI

from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class SearchNoteGUI(QWidget):
    def __init__(self, parent, action_after_search="none"):
        super().__init__()
        self.parent = parent
        self.controller = self.parent.controller
        self.action_after_search = action_after_search
        self.setWindowTitle("Search for Note")
        self.locked_in = False

        self.parent.setEnabled(False)

        layout = QGridLayout()

        if self.action_after_search != "none":
            label_info = QLabel("Enter Note code:")
        else:
            label_info = QLabel("Enter Note text contents or code:")

        self.text_info = QLineEdit()
        
        layout.addWidget(label_info, 0, 0)
        layout.addWidget(self.text_info, 0, 1)
        self.button_search = QPushButton("Search")
        layout.addWidget(self.button_search, 1, 0)
        self.button_cancel = QPushButton("Cancel")
        layout.addWidget(self.button_cancel, 1, 1)
        self.setLayout(layout)

        # connect the buttons' clicked signals to the slots below
        self.button_search.clicked.connect(self.search_button_clicked)
        self.button_cancel.clicked.connect(self.close)

    def search_button_clicked(self):
        # Searches for Note either by code or text content
        search_input = self.text_info.text()
        self.locked_in = False
        try: #see if input was an integer
            info = int(search_input)
            try:
                note = self.controller.search_note(info)
            except (NoCurrentPatientException):
                QMessageBox.warning(self, "Search Failure", "Cannot search for a note without a current patient!")
                self.close()
                return
            if note:
                QMessageBox.information(self, "Search Successful", f"Note found!")
                self.parent.refresh_by_search(info)
                if self.action_after_search == "update": #if "update", tell system to update note 
                    self.locked_in = True
                    self.create_edit_gui = CreateEditGui(self.parent, "Note", note)
                    self.create_edit_gui.show()
                elif self.action_after_search == "delete":
                    self.locked_in = True
                    delete_dialog = DeleteGUI(self.controller, "Note", info, self.parent)
                    delete_dialog.exec()
                    self.parent.refresh()
                self.close()
            else:
                QMessageBox.warning(self, "Search Failure", "Note not found!")
            
        except (ValueError): #if the input was not an integer, go here
            try: 
                note_list = self.controller.retrieve_notes(search_input)
            except (NoCurrentPatientException):
                QMessageBox.warning(self, "Search Failure", "Cannot search for a note without a current patient!")
                self.close()
                return
            if note_list and not self.update_after_search:
                QMessageBox.information(self, "Search Successful", "Notes found!")
                self.parent.refresh_by_retrieve(search_input)
                self.close()
            else:
                QMessageBox.warning(self, "Search Failure", "Notes not found!")

    def closeEvent(self, event):
        if self.action_after_search == "none" or not self.locked_in: #only enable if not set to have a follow-up prompt
            self.parent.setEnabled(True)