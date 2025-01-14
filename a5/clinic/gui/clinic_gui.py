import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QApplication, QMainWindow, QVBoxLayout, QGridLayout, QMenu, QAbstractItemView, QAbstractScrollArea, QPushButton, QTableView, QWidget, QDialog, QMessageBox, QMenuBar
from PyQt6.QtGui import QAction, QCursor

from clinic.controller import Controller
from clinic.patient import Patient

from clinic.gui.create_edit_gui import CreateEditGui
from clinic.gui.search_patient_gui import SearchPatientGUI
from clinic.gui.delete_gui import DeleteGUI

from clinic.gui.login_gui import LoginGUI
from clinic.gui.patient_table_model import PatientTableModel
from clinic.gui.note_menu_gui import NoteMenuGUI

class ClinicGUI(QMainWindow):

    def __init__(self, controller=None):
        super().__init__()
        if controller:
            self.controller = controller
        else:
            self.controller = Controller(autosave=True)

        # Add login GUI and prompt user login
        self.login_gui = LoginGUI(self.controller)
        self.prompt_login()

        self.setWindowTitle("Medical Clinic System - Main Menu")
        self.resize(600, 400)

        self.createMenuBar()
        # Add sub-window for notes menu and search patient
        self.search_patient_gui = SearchPatientGUI(self.controller, parent=self)
        self.note_menu_gui = None

        # Initialize table view to display all patients
        self.patient_table = QTableView()
        self.patient_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.patient_table.horizontalHeader().setStretchLastSection(True)

        self.patient_model = PatientTableModel(self.controller)
        self.patient_table.setModel(self.patient_model)

        # Add buttons for patient related actions
        create_button = QPushButton("Create Patient")
        create_button.clicked.connect(self.create_patient)
        refresh_button = QPushButton("List All Patients")
        refresh_button.clicked.connect(self.refresh)
        search_button = QPushButton("Search for Patients")
        search_button.clicked.connect(self.search_button_clicked)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_button_clicked)

        # Add necessary buttons and widgets to the main window
        layout = QVBoxLayout()
        layout.addWidget(self.patient_table)

        layout2 = QGridLayout()
        layout2.addWidget(create_button, 0, 0)
        layout2.addWidget(refresh_button, 1, 0)
        layout2.addWidget(search_button, 0, 1)
        layout2.addWidget(clear_button, 1, 1)

        layout.addLayout(layout2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def createMenuBar(self):
        # Create the main menu bar for the application
        menuBar = QMenuBar(self)

        userMenu = QMenu("User", self) #adds "User" to topbar
        menuBar.addMenu(userMenu)

        logoutAction = QAction("Logout", self) #adds action under User that allows user to logout
        userMenu.addAction(logoutAction)
        logoutAction.triggered.connect(self.logout)

        exitAction = QAction("Exit", self) #adds action under User that allows user to sys.exit
        userMenu.addAction(exitAction)
        exitAction.triggered.connect(sys.exit)

        helpMenu = QMenu("Help", self) #add "Help" to topbar
        menuBar.addMenu(helpMenu)

        explainAction = QAction("View Help Manual", self) #adds action under Help that allows user to open help manual
        helpMenu.addAction(explainAction)
        explainAction.triggered.connect(self.view_manual)

        self.setMenuBar(menuBar)

    def contextMenuEvent(self, event):
        selected_indexes = self.patient_table.selectionModel().selectedRows() # Gets currently selected rows in patient table
        if len(selected_indexes) > 0: # Check if there are any selected rows, if none, do not display the context menu
            self.menu = QMenu(self)

            viewNotes = QAction('View Notes', self)
            viewNotes.triggered.connect(self.view_notes)
            self.menu.addAction(viewNotes)

            editAction = QAction('Edit Patient', self)
            editAction.triggered.connect(self.edit_selected_patient)
            self.menu.addAction(editAction)

            deleteAction = QAction('Delete Patient', self)
            deleteAction.triggered.connect(self.delete_selected_patient)
            self.menu.addAction(deleteAction)

            # Add other required actions
            self.menu.popup(QCursor.pos()) # Puts menu at cursor position

    def prompt_login(self):
        self.login_gui.exec()
        if (self.login_gui.result() == 1): # login_gui is a QDialog, so by logging in and "accepting" the dialog, the result returns 1
            self.show() # Shows main window
        else:
            sys.exit() # Closes all tabs

    def logout(self):
        self.controller.logout() # Tells controller to logout
        self.close() # Closes main window
        self.prompt_login() # Causes login prompt to appear again
        
    def view_manual(self):
        QMessageBox.information(self, "Help Manual", "Thank you for using our Medical Clinic System!\n\nTo create, search or list all patients, please use the buttons found at the bottom of the main menu. To clear the table, please press the clear button found in the same area.\n\nTo view notes, edit or delete a patient, please right click on the patient's row and select the appropriate action. \n\nThe same ideas as above apply to notes; however, to access the notes menu you must right-click a patient and select \"view notes.\"")

    def create_patient(self): 
        # Opens create_edit_gui for creating a new patient 
        self.create_edit_gui = CreateEditGui(self, "Patient")
        self.create_edit_gui.show()

    def refresh(self):
        # Refreshes the data in the patient table
        self.patient_model.refresh_data()
        self.patient_table.setEnabled(True)

    def clear_button_clicked(self):
        # Clears the data in the patient table
        self.patient_model.reset()
        self.patient_table.setEnabled(False)

    def search_button_clicked(self):
        # Opens the search_patient_gui for finding specific patients
        self.search_patient_gui.show()

    def view_notes(self):
        selected_indexes = self.patient_table.selectionModel().selectedRows() # Gets currently selected rows in patient table
        selected_row = selected_indexes[0].row()

        phn = self.patient_model.data(self.patient_model.index(selected_row, 0), Qt.ItemDataRole.DisplayRole)
        if self.note_menu_gui: # If a note_menu_gui is already open, close it to avoid duplicates
            self.note_menu_gui.close()
        self.controller.set_current_patient(phn)

        self.note_menu_gui = NoteMenuGUI(self.controller) # Create note_menu_gui for current patient
        self.note_menu_gui.show()

    def edit_selected_patient(self):
        selected_indexes = self.patient_table.selectionModel().selectedRows() # Gets currently selected rows in patient table
        selected_row = selected_indexes[0].row()
        
        # Gets patient info from patient_model
        phn = self.patient_model.data(self.patient_model.index(selected_row, 0), Qt.ItemDataRole.DisplayRole)
        name = self.patient_model.data(self.patient_model.index(selected_row, 1), Qt.ItemDataRole.DisplayRole)
        dob = self.patient_model.data(self.patient_model.index(selected_row, 2), Qt.ItemDataRole.DisplayRole)
        phone = self.patient_model.data(self.patient_model.index(selected_row, 3), Qt.ItemDataRole.DisplayRole)
        email = self.patient_model.data(self.patient_model.index(selected_row, 4), Qt.ItemDataRole.DisplayRole)
        address = self.patient_model.data(self.patient_model.index(selected_row, 5), Qt.ItemDataRole.DisplayRole)

        patient = Patient(phn, name, dob, phone, email, address)

        # Open a create_edit_gui pre-filled with the patient's info for editing
        self.create_edit_gui = CreateEditGui(self, "Patient", patient)
        self.create_edit_gui.show()

    def delete_selected_patient(self):
        selected_indexes = self.patient_table.selectionModel().selectedRows() # Gets currently selected rows in patient table
        selected_row = selected_indexes[0].row()
        
        # Gets PHN of the patient to be deleted
        phn = self.patient_model.data(self.patient_model.index(selected_row, 0), Qt.ItemDataRole.DisplayRole)

        # Opens confirmation dialog for deleting the patient
        delete_dialog = DeleteGUI(self.controller, "Patient", phn, self)
        delete_dialog.exec()
        self.patient_model.redo_refresh() # Refreshes patient table after deletion

    def closeEvent(self, event): # When pressing the X button in the top right, this event will trigger
        QApplication.closeAllWindows() #closes all tabs. cant have anything open if main window is closed

def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    app.exec()

if __name__ == '__main__':
    main()
