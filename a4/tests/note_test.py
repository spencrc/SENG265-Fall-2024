from unittest import TestCase
from unittest import main
from clinic.note import *

class NoteTest(TestCase):
    def setUp(self):
        self.note = Note(1, "Note")
    def test_equality(self):
        note1a = Note(1, "Note")
        note1b = Note(1, "Not Note")
        note2a = Note(2, "Note")
        note2b = Note(2, "Not Note")

        self.assertEqual(self.note, note1a, "self.note and note1a are equal")
        self.assertNotEqual(self.note, note1b, "same code, but different text contents so self.note and note1b are not equal")
        self.assertNotEqual(self.note, note2a, "different code, same text between self.note and note2a so not equal")
        self.assertNotEqual(self.note, note2b, "different code and different text, self.note and note2b are not equal")
        self.assertNotEqual(self.note, None, "cannot compare to None, self.note and None are not equal")

    def test_timestamp(self):
        self.assertNotEqual(self.note.timeStamp, datetime.now, "can't match if was created sometime before")
        self.assertTrue(type(self.note.timeStamp) is datetime, "timeStamp is of type datetime")

        self.note.update_datetime()
        self.assertTrue(type(self.note.timeStamp) is datetime, "timeStamp is of type datetime")