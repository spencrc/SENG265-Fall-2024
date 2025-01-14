from clinic.patient_record import PatientRecord
from clinic.note import Note

class Patient:
    def __init__(self, phn: int = 0, name: str = "", birth_date: str = "", phone: str = "", email: str = "", address: str = "", autosave=False):
        self.phn = phn
        self.name = name 
        self.birth_date = birth_date 
        self.phone = phone 
        self.email = email 
        self.address = address 
        self.record = PatientRecord(autosave, phn)

    def __str__(self) -> str:
        return ("phn: " + str(self.phn) + " name: " + self.name + " dob: " + self.birth_date + " phone: " + self.phone + " email: " + self.email + " address: " + self.address)
    
    def __eq__(self, other) -> bool:
        if other == None:
            return False
        elif (self.phn == other.phn and self.name == other.name and self.birth_date == other.birth_date and self.phone == other.phone and self.email == other.email and self.address == other.address):
            return True
        else :
            return False
        
    def create_note(self, text: str) -> Note:
        return self.record.create_note(text) #goes down chain of delegation
    
    def search_note(self, code: int) -> Note: 
        return self.record.search_note(code) #goes down chain of delegation
    
    def retrieve_notes(self, keyword: str) -> list:
        return self.record.retrieve_notes(keyword) #goes down chain of delegation
    
    def update_note(self, code: int, text: str) -> bool:
        return self.record.update_note(code, text) #goes down chain of delegation
    
    def delete_note(self, code: int) -> bool:
        return self.record.delete_note(code) #goes down chain of delegation
    
    def list_notes(self) -> list:
        return self.record.list_notes() #goes down chain of delegation