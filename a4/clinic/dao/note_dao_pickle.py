from pickle import load, dump
from clinic.dao.note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    def __init__(self, autosave=False):
        self.autosave = autosave
        self.filename = '' #empty on initialization
        self.notes = []
        self.autocounter = 0

    def unpickle_notes(self, phn: int) -> list: #loads notes of patient given a phn
        self.filename = 'clinic/records/' + str(phn) + '.dat' #sets file path for clinic/records/<PHN>.dat
        try:
            with open(self.filename, 'rb') as file: #reads binary from file path
                self.notes = load(file) #stores all data in unpickled file in self.notes
                if len(self.notes) > 0: #not possible to index at -1 in python if the list is empty
                    self.autocounter = self.notes[-1].code #gets last element in list
                else:
                    self.autocounter = 0 #empty list, so autocounter must be zero
        except FileNotFoundError:
            self.notes = [] #if no file, set to empty list


    def pickle_notes(self) -> None:
        with open(self.filename, 'wb') as file: #writes as binary to file path
                dump(self.notes, file) #pickles self.notes into file path

    def create_note(self, text: str) -> Note: #creates a new note object, adds it to notes and returns the object
        self.autocounter += 1
        newNote = Note(self.autocounter, text)
        self.notes.append(newNote)
        if self.autosave:
            self.pickle_notes()
        return newNote
    
    def search_note(self, code: int) -> Note: #searches through notes for a note with a code as given in input. returns note matching code or returns None
        for note in self.notes:
                if note.code == code:
                    return note
        return None
    
    def retrieve_notes(self, keyword: str) -> list: #searches through notes for all note objects containing a keyword in its text, then returns the list of notes that have the keyword
        retrieved_list = []
        for note in self.notes:
            if keyword in note.text:
                retrieved_list.append(note)
        return retrieved_list
    
    def update_note(self, code: int, text: str) -> bool: #if there is no note with the input code, cannot update. otherwise, update text and timestamp and return true
        if self.search_note(code) == None:
            return False
        else:
            note = self.search_note(code)
            note.text = text
            note.timeStamp = note.update_datetime()
            if self.autosave:
                self.pickle_notes()
        return True #if-else statement beforehand makes sure this only returns true if correct conditions are met, up to preference to be indented 
    
    def delete_note(self, code: int) -> bool: #makes sure notes is not empty and there is a note object with the input code. if there is, loop through notes to find the note with the input code to remove it
        if len(self.notes) == 0 or self.search_note(code) == None:
            return False
        else:
            for note in self.notes:
                if note.code == code:
                    self.notes.remove(note)
                    if self.autosave:
                        self.pickle_notes()
                    break #job is done, break out of loop
        return True #if-else statement beforehand makes sure this only returns true if correct conditions are met, up to preference to be indented 
    
    def list_notes(self) -> list: #formats notes for output by adding all objects in notes to new list, then returns contents of new list
        output_list = []
        for note in self.notes:
            output_list.insert(0, note)
        return output_list 