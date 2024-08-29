import unittest
from models.bed import Bed, BedType
from enum import Enum



class TestBed(unittest.TestCase):
    def setUp(self):
        self.bed = Bed(bed_id=1)

    def test_initialization(self):
        self.assertEqual(self.bed.bed_id, 1)
        self.assertEqual(self.bed.bed_type, BedType.REGULAR)
        self.assertFalse(self.bed.is_occupied)
        self.assertIsNone(self.bed.current_patient)

    def test_add_patient(self):
        self.bed.add_patient('John Doe')
        self.assertTrue(self.bed.is_occupied)
        self.assertEqual(self.bed.current_patient, 'John Doe')

    def test_discharge_patient(self):
        self.bed.add_patient('John Doe')
        self.bed.discharge_patient()
        self.assertFalse(self.bed.is_occupied)
        self.assertIsNone(self.bed.current_patient)

    def test_add_patient_when_occupied(self):
        self.bed.add_patient('John Doe')
        with self.assertRaises(Exception) as context:
            self.bed.add_patient('Jane Doe')
        self.assertEqual(str(context.exception), "Bed is already occupied")

    def test_discharge_patient_when_not_occupied(self):
        with self.assertRaises(Exception) as context:
            self.bed.discharge_patient()
        self.assertEqual(str(context.exception), "Bed is not occupied")

    def test_update_bed_type(self):
        self.bed.update_bed_type(BedType.ICU)
        self.assertEqual(self.bed.bed_type, BedType.ICU)

    def test_update_bed_type_invalid(self):
        with self.assertRaises(ValueError) as context:
            self.bed.update_bed_type('InvalidType')
        self.assertEqual(str(context.exception), "new_type must be an instance of BedType")

if __name__ == '__main__':
    unittest.main()

if __name__ == "__main__":
    unittest.main()
