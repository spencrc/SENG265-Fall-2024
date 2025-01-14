from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QMessageBox

from clinic.exception.illegal_access_exception import IllegalAccessException

class PatientTableModel(QAbstractTableModel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.last_refresh_func = self.refresh_data
        self.last_arg = None
        self._data = []
        self.refresh_data()

    def refresh_data(self):
        # Refreshes all patients
        try:
            self._data = []
            patient_list = self.controller.list_patients()
            for patient in patient_list:
                # Converts patient objects into displayable values
                listified_patient = []
                listified_patient.append(patient.phn)
                listified_patient.append(patient.name)
                listified_patient.append(patient.birth_date)
                listified_patient.append(patient.phone)
                listified_patient.append(patient.email)
                listified_patient.append(patient.address)
                self._data.append(listified_patient)

            self.layoutChanged.emit() # emit the layoutChanged signal to alert the QTableView of model changes
            self.last_refresh_func = self.refresh_data
            self.last_arg = None
        except (IllegalAccessException): # Handles access error if user is not logged in
            QMessageBox.critical(None, "Access Denied", "You must be logged in to view patients.")
            self.set_patients([])  # Set an empty list to prevent crashes
    
    def refresh_via_search(self, phn):
        # Refreshes data by searching for patient by PHN
        self._data = []
        patient = self.controller.search_patient(phn)
        if patient:
        # Converts patient objects into displayable values
            listified_patient = []
            listified_patient.append(patient.phn)
            listified_patient.append(patient.name)
            listified_patient.append(patient.birth_date)
            listified_patient.append(patient.phone)
            listified_patient.append(patient.email)
            listified_patient.append(patient.address)
            self._data.append(listified_patient)
            self.layoutChanged.emit()
            self.last_refresh_func = self.refresh_via_search
            self.last_arg = phn
        else:
            # Shows warning if patient not found
            QMessageBox.warning(self, "Search Failed", "Patient not found")

    def refresh_via_retrieve(self, name):
        # Refreshes data by searching for patient containing name
        self._data = []
        patient_list = self.controller.retrieve_patients(name)
        for patient in patient_list:
            listified_patient = []
            listified_patient.append(patient.phn)
            listified_patient.append(patient.name)
            listified_patient.append(patient.birth_date)
            listified_patient.append(patient.phone)
            listified_patient.append(patient.email)
            listified_patient.append(patient.address)
            self._data.append(listified_patient)
            self.last_refresh_func = self.refresh_via_retrieve
            self.last_arg = name
        self.layoutChanged.emit()
            
    def redo_refresh(self):
        # Re-do the last refresh with its arguments
        if self.last_arg:
            self.last_refresh_func(self.last_arg)
        else:
            self.last_refresh_func()

    def reset(self):
        # Clears all table data
        self._data = []
        # emit the layoutChanged signal to alert the QTableView of model changes
        self.layoutChanged.emit()

    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            # Perform per-type checks and render accordingly.
            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value
            # Default (anything not captured above: e.g. int)
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int):
                # Align right, vertical middle.
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ['PHN', 'Name', 'Birthdate', 'Phone Number', 'Email Address', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)