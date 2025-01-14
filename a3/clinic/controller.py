from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note

class Controller:
    
    def __init__(self):
        self.username = "user"
        self.password = "clinic2024"
        self.logged = False
        self.currentPatient = None
        self.patients = []
        
    def is_logged(self) -> bool: #just returns boolean value of logged field
        return self.logged

    def login(self, username, password) -> None:
        if self.logged == True: #cannot login if already logged in
            return False
        elif self.username == username and self.password == password: #have to have correct username and password to login
            self.logged = True
        return self.is_logged() #returns true is username and password were correct, otherwise false

    def logout(self) -> None:
        if self.logged == False: #cannot logout if already logged out
            return False
        else: #successfully can log out
            self.logged = False
            return True

    def search_patient(self, phn: int) -> Patient:
        if not self.logged: # cannot access patients if not logged in
            return None
        for patient in self.patients:
            if patient.phn == phn:
                return patient
        return None
        
    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> Patient:
        if not self.logged: # cannot create patient if not logged in 
            return None
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        if self.search_patient(new_patient.phn) == None: # patient cannot be created if it already exists
            self.patients.append(new_patient)
        else:
            return None
        return new_patient

    def retrieve_patients(self, name: str) -> list:
        if not self.logged: # cannot access patients if not logged in 
            return None
        patients_with_name = []
        for patient in self.patients:
            if name.lower() in patient.name.lower():
                patients_with_name.append(patient)
        return patients_with_name
    
    def update_patient(self, phn1: int, phn2: int, name: str, birth_date: str, phone: str, email: str, address: str) -> bool:
        if(self.currentPatient != None and self.currentPatient.phn == phn1): # cannot update currentPatient or patient if another patient has the new PHN
            return False
        if phn1 != phn2:
            for patient in self.patients:
                if patient.phn == phn2:
                    return False # cannot update patient with registered PHN
        for patient in self.patients:
            if patient.phn == phn1:
                patient.phn = phn2
                patient.name = name
                patient.birth_date = birth_date
                patient.phone = phone
                patient.email = email
                patient.address = address
                return True
        return False
    
    def delete_patient(self, phn: int) -> bool:
        if not self.logged: # cannot access currentPatient if not logged in
            return None
        if self.get_current_patient() and self.get_current_patient().phn == phn: # cannot delete current patient
            return False
        initial_length = len(self.patients)
        self.patients = [patient for patient in self.patients if patient.phn != phn] # make list of all patients except ones with target PHN
        return len(self.patients) < initial_length # deletion is successful if new list doesnt contain patient with target PHN
        
    def list_patients(self) -> list:
        if not self.logged: # cannot access patients if not logged in
          return None
        return self.patients
    
    def get_current_patient(self) -> Patient:
        if not self.logged: # cannot access currentPatient if not logged in
            return None
        return self.currentPatient
    
    def set_current_patient(self, phn: int)  -> bool:
        if not self.logged: # cannot access patients if not logged in
            return None
        for patient in self.patients:
            if patient.phn == phn:
                self.currentPatient = patient
                return True
        return False # fails if patient with target PHN is not found
    
    def unset_current_patient(self):
        if not self.logged: # cannot access currentPatient if not logged in
            return None
        self.currentPatient = None
    
    def create_note(self, text: str) -> Note:
        if not self.logged or self.currentPatient == None: #cannot create note if not logged in or no currentPatient
            return None
        else:
            return self.currentPatient.create_note(text) #goes down chain of delegation
    
    def search_note(self, code: int) -> Note:
        if not self.logged or self.currentPatient == None: #cannot create note if not logged in or no currentPatient
            return None
        else:
            return self.currentPatient.search_note(code) #goes down chain of delegation
        
    def retrieve_notes(self, keyword: str) -> list:
        if not self.logged or self.currentPatient == None: #cannot create note if not logged in or no currentPatient
            return None
        else: 
            return self.currentPatient.retrieve_notes(keyword) #goes down chain of delegation

    def update_note(self, code: int, text: str) -> bool:
        if not self.logged or self.currentPatient == None: #cannot create note if not logged in or no currentPatient
            return None
        else:
            return self.currentPatient.update_note(code, text) #goes down chain of delegation

    def delete_note(self, code: int) -> bool:
         if not self.logged or self.currentPatient == None: #cannot create note if not logged in or no currentPatient
            return None
         else:
            return self.currentPatient.delete_note(code) #goes down chain of delegation
         
    def list_notes(self) -> list:
        if not self.logged or self.currentPatient == None: #cannot create note if not logged in or no currentPatient
            return None
        else:
            return self.currentPatient.list_notes() #goes down chain of delegation