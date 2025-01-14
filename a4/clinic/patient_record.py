from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    def __init__(self, autosave, phn=None):
        self.note_dao = NoteDAOPickle(autosave)
        if autosave:
            self.note_dao.unpickle_notes(phn)

    def create_note(self, text: str) -> Note:
        return self.note_dao.create_note(text)
    
    def search_note(self, code: int) -> Note: 
        return self.note_dao.search_note(code)
    
    def retrieve_notes(self, keyword: str) -> list: 
        return self.note_dao.retrieve_notes(keyword)
    
    def update_note(self, code: int, text: str) -> bool: 
        return self.note_dao.update_note(code, text)
    
    def delete_note(self, code: int) -> bool: 
        return self.note_dao.delete_note(code)
    
    def list_notes(self) -> list:
        return self.note_dao.list_notes()