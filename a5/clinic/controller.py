from clinic.patient import Patient
from clinic.note import Note
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
import hashlib
from clinic.dao.patient_dao_json import PatientDAOJSON

class Controller:
    
    def __init__(self, autosave = False):
        self.users = self.get_users()
        self.autosave = autosave
        self.logged = False
        self.patient_dao = PatientDAOJSON(autosave)

    def get_users(self) -> dict:
        users = {}
        with open('clinic/users.txt', 'r') as file:
            for line in file:
                line = line.strip()
                contents = line.split(',')
                users[contents[0]] = contents[1]

        return users
        
    def is_logged(self) -> bool: #just returns boolean value of logged field
        return self.logged
    
    def get_password_hash(self, password: str) -> str: #from lab9
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig

    def login(self, username: str, password: str) -> bool:
        if self.logged == True: #cannot login if already logged in
            raise DuplicateLoginException
        elif self.users.get(username): #have to have valid username
            attempted_password = self.get_password_hash(password) #converts attempted password into hash via lab9 code
            if attempted_password == self.users.get(username):
                self.logged = True
                return True
        raise InvalidLoginException

    def logout(self) -> None:
        if self.logged == False: #cannot logout if already logged out
            raise InvalidLogoutException
        else: #successfully can log out
            self.logged = False
            return True

    def search_patient(self, phn: int) -> Patient:
        if not self.logged: # cannot access patients if not logged in
            raise IllegalAccessException
        return self.patient_dao.search_patient(phn)
        
    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> Patient:
        if not self.logged: # cannot create patient if not logged in 
            raise IllegalAccessException
        return self.patient_dao.create_patient(phn, name, birth_date, phone, email, address)

    def retrieve_patients(self, name: str) -> list:
        if not self.logged: # cannot access patients if not logged in 
            raise IllegalAccessException
        return self.patient_dao.retrieve_patients(name)
    
    def update_patient(self, phn1: int, phn2: int, name: str, birth_date: str, phone: str, email: str, address: str) -> bool:
        if not self.logged:
            raise IllegalAccessException
        return self.patient_dao.update_patient(phn1, phn2, name, birth_date, phone, email, address)
    
    def delete_patient(self, phn: int) -> bool:
        if not self.logged: # cannot access currentPatient if not logged in
            raise IllegalAccessException
        return self.patient_dao.delete_patient(phn)
        
    def list_patients(self) -> list:
        if not self.logged: # cannot access patients if not logged in
          raise IllegalAccessException
        return self.patient_dao.list_patients()
    
    def get_current_patient(self) -> Patient:
        if not self.logged: # cannot access currentPatient if not logged in
            raise IllegalAccessException
        return self.patient_dao.get_current_patient()
    
    def set_current_patient(self, phn: int)  -> bool:
        if not self.logged: # cannot access patients if not logged in
            raise IllegalAccessException
        return self.patient_dao.set_current_patient(phn)
    
    def unset_current_patient(self):
        if not self.logged: # cannot access currentPatient if not logged in
            raise IllegalAccessException
        return self.patient_dao.unset_current_patient()
    
    def create_note(self, text: str) -> Note:
        if not self.logged: #cannot create note if not logged in or no currentPatient
            raise IllegalAccessException
        elif self.patient_dao.get_current_patient() == None:
            raise NoCurrentPatientException
        else:
            return self.patient_dao.get_current_patient().create_note(text) #goes down chain of delegation
    
    def search_note(self, code: int) -> Note:
        if not self.logged: #cannot create note if not logged in or no currentPatient
            raise IllegalAccessException
        elif self.patient_dao.get_current_patient() == None:
            raise NoCurrentPatientException
        else:
            return self.patient_dao.get_current_patient().search_note(code) #goes down chain of delegation
        
    def retrieve_notes(self, keyword: str) -> list:
        if not self.logged: #cannot create note if not logged in or no currentPatient
            raise IllegalAccessException
        elif self.patient_dao.get_current_patient() == None:
            raise NoCurrentPatientException
        else: 
            return self.patient_dao.get_current_patient().retrieve_notes(keyword) #goes down chain of delegation

    def update_note(self, code: int, text: str) -> bool:
        if not self.logged: #cannot create note if not logged in or no currentPatient
            raise IllegalAccessException
        elif self.patient_dao.get_current_patient() == None:
            raise NoCurrentPatientException
        else:
            return self.patient_dao.get_current_patient().update_note(code, text) #goes down chain of delegation

    def delete_note(self, code: int) -> bool:
        if not self.logged: #cannot create note if not logged in or no currentPatient
            raise IllegalAccessException
        elif self.patient_dao.get_current_patient() == None:
            raise NoCurrentPatientException
        else:
            return self.patient_dao.get_current_patient().delete_note(code) #goes down chain of delegation
         
    def list_notes(self) -> list:
        if not self.logged: #cannot create note if not logged in or no currentPatient
            raise IllegalAccessException
        elif self.patient_dao.get_current_patient() == None:
            raise NoCurrentPatientException
        else:
            return self.patient_dao.get_current_patient().list_notes() #goes down chain of delegation