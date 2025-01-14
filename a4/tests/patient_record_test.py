from unittest import TestCase
from unittest import main
from clinic.patient_record import *

class PatientRecordTest(TestCase):
    def setUp(self):
        self.record = PatientRecord()

    def test_create_note(self):
        expected_note_1 = Note(1, "Note 1.")
        expected_note_2 = Note(2, "Note 2.")
        expected_note_3 = Note(3, "Note 3.")

        #Tests if autocounter is 1
        Note1 = self.record.create_note("Note 1.")
        self.assertEqual(self.record.autocounter, 1, "autocounter is 1")
        self.assertTrue(expected_note_1 == Note1, "Note1 matches expected note 1")
        
        #Tests if autocounter is 2
        Note2 = self.record.create_note("Note 2.")
        self.assertEqual(self.record.autocounter, 2, "autocounter is 2")
        self.assertTrue(expected_note_2 == Note2, "Note2 matches expected note 2")

        #Tests if autocounter is 3
        Note3 = self.record.create_note("Note 3.")
        self.assertEqual(self.record.autocounter, 3, "autocounter is 3")
        self.assertTrue(expected_note_3 == Note3, "Note3 matches expected note 3")

    def test_search_note(self):
        expected_note_1 = Note(1, "Note 1.")
        expected_note_2 = Note(2, "Note 2.")
        expected_note_3 = Note(3, "Note 3.")

        #Search for note 1 before it exists
        self.assertIsNone(self.record.search_note(1), "Note does not exist yet")

        #Create notes
        Note1 = self.record.create_note("Note 1.")
        Note2 = self.record.create_note("Note 2.")
        Note3 = self.record.create_note("Note 3.")

        #Make sure notes were made and stored correctly
        actual_note_1 = self.record.search_note(1)
        actual_note_2 = self.record.search_note(2)
        actual_note_3 = self.record.search_note(3)
        self.assertIsNotNone(actual_note_1, "Note 1 was found")
        self.assertIsNotNone(actual_note_2, "Note 2 was found")
        self.assertIsNotNone(actual_note_3, "Note 3 was found")

        #Make sure non-existent note is not being... somehow found
        self.assertIsNone(self.record.search_note(4), "Note 4 shouldn't exist")

        #Make sure notes match 
        self.assertEqual(actual_note_1, expected_note_1, "Note 1 expected and actual match")
        self.assertEqual(actual_note_2, expected_note_2, "Note 2 expected and actual match")
        self.assertEqual(actual_note_3, expected_note_3, "Note 1 expected and actual match")

    def test_retrieve_update_delete_and_list_notes(self):
        notes_list = self.record.list_notes()
        self.assertEqual(len(notes_list), 0, "list of notes has size 0")

        Note1 = self.record.create_note("Note 1. hello hello hello")
        Note2 = self.record.create_note("Note 2.")
        Note3 = self.record.create_note("Note 3.")
        Note4 = self.record.create_note("Note 4. hello")
        Note5 = self.record.create_note("hello")

        notes_list = self.record.list_notes()
        self.assertEqual(len(notes_list), 5, "list of notes has size 5")

        #Test if notes retrieved correctly
        retrieved_notes = self.record.retrieve_notes("hello")
        self.assertEqual(len(retrieved_notes), 3, "3 notes with keyword hello")

        #Update notes
        self.assertTrue(self.record.update_note(1, "Note 1."), "update on Note 1")
        self.assertTrue(self.record.update_note(4, "Note 4."), "update on Note 4")
        self.assertTrue(self.record.update_note(5, "Note 5."), "update on Note 5")
        self.assertFalse(self.record.update_note(6, "Note 6."), "update on Note 6 failed")
        self.assertFalse(self.record.update_note(7, "Note 7."), "update on Note 7 failed")

        #Test if notes retrieved correctly
        retrieved_notes = self.record.retrieve_notes("hello")
        self.assertEqual(len(retrieved_notes), 0, "0 notes with keyword hello")
        
        #Delete some notes
        self.assertTrue(self.record.delete_note(1), "delete Note 1")
        self.assertTrue(self.record.delete_note(4), "delete Note 4")
        self.assertTrue(self.record.delete_note(3), "delete Note 3")
        self.assertFalse(self.record.delete_note(7), "attempt delete on non-existent Note 7")
        self.assertFalse(self.record.delete_note(6), "attempt delete on non-existent Note 6")

        notes_list = self.record.list_notes()
        self.assertEqual(len(notes_list), 2, "list of notes has size 2")

        #Double-checking deletes worked
        self.assertIsNone(self.record.search_note(1), "Note 1 was deleted")
        self.assertIsNone(self.record.search_note(4), "Note 4 was deleted")
        self.assertIsNone(self.record.search_note(3), "Note 3 was deleted")
        self.assertIsNotNone(self.record.search_note(2), "Note 2 was not deleted")
        self.assertIsNotNone(self.record.search_note(5), "Note 5 was not deleted")

        Note6 = self.record.create_note("Note 6.")
        Note7 = self.record.create_note("Note 7.")

        #Last retrieve note and list note check
        notes_list = self.record.list_notes()
        self.assertEqual(len(notes_list), 4, "list of notes has size 4")
        retrieved_notes = self.record.retrieve_notes("Note")
        self.assertEqual(len(retrieved_notes), 4, "4 notes with keyword Note")