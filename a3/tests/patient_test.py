from unittest import TestCase
from unittest import main
from clinic.patient import *

class PatientTest(TestCase):
    def setUp(self):
        self.patient = Patient()
    def test_equality(self): 
        patient1 = Patient(9790012000, "Jane Remover", "2000-10-10", "250 203 1010", "jane.remover@gmail.com", "300 Moss St, Victoria")
        patient1a = Patient(9790012000, "Jane Remover", "2000-10-10", "250 203 1010", "jane.remover@gmail.com", "300 Moss St, Victoria")

        patient2 = Patient(9790014444, "Porter Robinson", "1995-07-01", "250 203 2020", "probinson@gmail.com", "300 Moss St, Victoria")
        patient2a = Patient(9790019800, "Porter Robinson", "2005-09-24", "250 216 1234", "robinson.porter@gmail.com", "3800 Finnerty Rd, Victoria")  # same name, everything else different
        patient2b = Patient(9790014444, "Benjamin Reichwald", "1982-05-05", "250 208 2189", "benji@gmail.com", "333 Gravity St, Victoria")
        patient3 = Patient(9792225555, "Eckoh Tookay", "1990-01-15", "278 456 7890", "2k.ecco@outlook.com", "5000 Douglas St, Saanich")

        # Test for identical patients
        self.assertEqual(patient1, patient1a, "Identical patients should be equal")

        # Test for patients with the same name but otherwise different attributes
        self.assertNotEqual(patient2, patient2a, "Patients with the same name but different details should not be equal")
    
        # Test for completely different patients
        self.assertNotEqual(patient2, patient3, "Different patients should not be equal")

        # Additional checks to ensure robustness
        self.assertNotEqual(patient1, patient2, "Different patients should not be equal")
        self.assertNotEqual(patient2, patient2b, "Patients with the same PHN but different names should not be equal")
        self.assertNotEqual(patient2a, patient2b, "Completely different patients should not be equal")
        
    def test_string(self):
        patient = Patient(9790012000, "Jane Remover", "2000-10-10", "250 203 1010", "jane.remover@gmail.com", "300 Moss St, Victoria")
        expected_str = "phn: 9790012000 name: Jane Remover dob: 2000-10-10 phone: 250 203 1010 email: jane.remover@gmail.com address: 300 Moss St, Victoria"
        self.assertEqual(str(patient), expected_str, "The string representation of the patient is incorrect")

        # Test with a different patient
        patient2 = Patient(9790014444, "Porter Robinson", "1995-07-01", "250 203 2020", "probinson@gmail.com", "300 Moss St, Victoria")
        expected_str2 = "phn: 9790014444 name: Porter Robinson dob: 1995-07-01 phone: 250 203 2020 email: probinson@gmail.com address: 300 Moss St, Victoria"
        self.assertEqual(str(patient2), expected_str2, "The string representation of the second patient is incorrect")

        # Test with default patient
        default_patient = Patient()
        expected_default_str = "phn: 0 name:  dob:  phone:  email:  address: "
        self.assertEqual(str(default_patient), expected_default_str, "The string representation of the default patient is incorrect")