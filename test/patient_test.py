import unittest
from models.bed import Bed, BedType
from models.patient import Patient


class TestBed(unittest.TestCase):

    def setUp(self):
        # Initialize Bed and Patient objects before each test
        self.bed1 = Bed(bed_id=1)
        self.patient = Patient(patient_id=1, name="John Doe", age=30, status="Stable")

    def test_bed_initialization(self):
        # Test initialization of Bed object
        self.assertEqual(self.bed1.bed_id, 1)
        self.assertEqual(self.bed1.bed_type, BedType.REGULAR)
        self.assertFalse(self.bed1.is_occupied)
        self.assertIsNone(self.bed1.current_patient)

    def test_add_patient(self):
        # Test adding a patient to a bed
        self.bed1.add_patient(self.patient)
        self.assertTrue(self.bed1.is_occupied)
        self.assertEqual(self.bed1.current_patient, self.patient)

    def test_add_patient_when_occupied(self):
        # Test adding a patient when the bed is already occupied
        self.bed1.add_patient(self.patient)
        with self.assertRaises(Exception) as context:
            self.bed1.add_patient(self.patient)  # Trying to add another patient
        self.assertTrue('Bed is already occupied' in str(context.exception))

    def test_discharge_patient(self):
        # Test discharging a patient from a bed
        self.bed1.add_patient(self.patient)  # First, occupy the bed
        self.bed1.discharge_patient()
        self.assertFalse(self.bed1.is_occupied)
        self.assertIsNone(self.bed1.current_patient)

    def test_discharge_patient_when_not_occupied(self):
        # Test discharging a patient when the bed is not occupied
        with self.assertRaises(Exception) as context:
            self.bed1.discharge_patient()
        self.assertTrue('Bed is not occupied' in str(context.exception))



if __name__ == "__main__":
    unittest.main()
