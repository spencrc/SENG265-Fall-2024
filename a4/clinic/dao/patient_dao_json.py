import json
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.dao.patient_dao import PatientDAO
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.patient import Patient
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave=False):
        self.autosave = autosave
        self.filename = 'clinic/patients.json'
        if self.autosave:
          try:
              with open(self.filename, 'r') as file: #opens clinic/patients.json file for reading, decodes according to PatientDecoder and stores in self.patients
                  self.patients = json.load(file, cls=PatientDecoder)
          except (FileNotFoundError, json.JSONDecodeError):
              self.patients = [] #if no file, empty list
        else:
            self.patients = []
        self.currentPatient = None


    #implement all delegated methods (read assignment pdf and lecture 26)
    def search_patient(self, phn: int) -> Patient:
        for patient in self.patients:
            if patient.phn == phn:
                return patient
        return None
        
    def dump_json(self): #opens clinic/patients.json file for writing and writes via dumping it using PatientEncoder as its encoding class
        with open(self.filename, 'w') as file:
            json.dump(self.patients, file, cls=PatientEncoder)

    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> Patient:
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        if self.search_patient(new_patient.phn) == None: # patient cannot be created if it already exists
            self.patients.append(new_patient)
            if self.autosave:
                self.dump_json()
        else:
            raise IllegalOperationException
        return new_patient

    def retrieve_patients(self, name: str) -> list:
        patients_with_name = []
        for patient in self.patients:
            if name.lower() in patient.name.lower():
                patients_with_name.append(patient)
        return patients_with_name
    
    def update_patient(self, phn1: int, phn2: int, name: str, birth_date: str, phone: str, email: str, address: str) -> bool:
        if(self.currentPatient != None and self.currentPatient.phn == phn1): # cannot update currentPatient or patient if another patient has the new PHN
            raise IllegalOperationException
        if phn1 != phn2:
            for patient in self.patients:
                if patient.phn == phn2:
                    raise IllegalOperationException # cannot update patient with registered PHN
        for patient in self.patients:
            if patient.phn == phn1:
                patient.phn = phn2
                patient.name = name
                patient.birth_date = birth_date
                patient.phone = phone
                patient.email = email
                patient.address = address
                if self.autosave:
                    self.dump_json()
                return True
        raise IllegalOperationException
    
    def delete_patient(self, phn: int) -> bool:
        if self.get_current_patient() and self.get_current_patient().phn == phn: # cannot delete current patient
            raise IllegalOperationException
        initial_length = len(self.patients)
        self.patients = [patient for patient in self.patients if patient.phn != phn] # make list of all patients except ones with target PHN
        successful = len(self.patients) < initial_length
        if successful:
            if self.autosave:
                self.dump_json()
            return len(self.patients) < initial_length # deletion is successful if new list doesnt contain patient with target PHN
        else:
            raise IllegalOperationException
        
    def list_patients(self) -> list:
        return self.patients
    
    def get_current_patient(self) -> Patient:
        return self.currentPatient
    
    def set_current_patient(self, phn: int)  -> bool:
        for patient in self.patients:
            if patient.phn == phn:
                self.currentPatient = patient
                return True
        raise IllegalOperationException # fails if patient with target PHN is not found
    
    def unset_current_patient(self):
        self.currentPatient = None

    