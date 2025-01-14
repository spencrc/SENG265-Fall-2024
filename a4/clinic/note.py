from datetime import datetime

class Note:
    def __init__(self, code: int, text: str):
        self.code = code
        self.text = text
        self.timeStamp = datetime.now()

    def __eq__(self, other):
        if other == None:
            return False
        elif self.code == other.code and self.text == other.text:
            return True
        else:
            return False
        
    def update_datetime(self) -> datetime:
        self.timeStamp = datetime.now()
        