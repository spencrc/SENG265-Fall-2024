from datetime import datetime

class Note:
    def __init__(self, code: int, text: str):
        self.code = code
        self.text = text
        self.timestamp = datetime.now()

    def __eq__(self, other):
        if other == None:
            return False
        elif self.code == other.code and self.text == other.text:
            return True
        else:
            return False
        
    def __str__(self):
        return 'Note #%d, from %s: %s' % (self.code, self.timestamp, self.text)
        
    def update_datetime(self) -> datetime:
        self.timestamp = datetime.now()
        