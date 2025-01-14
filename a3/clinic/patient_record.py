from clinic.note import Note

class PatientRecord:
    def __init__(self):
        self.autocounter = 0
        self.notes = []

    def create_note(self, text: str) -> Note: #creates a new note object, adds it to notes and returns the object
        self.autocounter += 1
        newNote = Note(self.autocounter, text)
        self.notes.append(newNote)
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
        return True #if-else statement beforehand makes sure this only returns true if correct conditions are met, up to preference to be indented 
    
    def delete_note(self, code: int) -> bool: #makes sure notes is not empty and there is a note object with the input code. if there is, loop through notes to find the note with the input code to remove it
        if len(self.notes) == 0 or self.search_note(code) == None:
            return False
        else:
            for note in self.notes:
                if note.code == code:
                    self.notes.remove(note)
                    break #job is done, break out of loop
        return True #if-else statement beforehand makes sure this only returns true if correct conditions are met, up to preference to be indented 
    
    def list_notes(self) -> list: #formats notes for output by adding all objects in notes to new list, then returns contents of new list
        output_list = []
        for note in self.notes:
            output_list.insert(0, note)
        return output_list 