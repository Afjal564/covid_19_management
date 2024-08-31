import unittest

from models.Hospital import Hospital


class TestHospital(unittest.TestCase):
    def setUp(self):
        self.hospital = Hospital(name="City Hospital", pin_code="12345")

    def test_add_patient(self):
        self.hospital.add_patient("John Doe")
        self.assertIn("John Doe", self.hospital.patients)

    def test_discharge_patient(self):
        self.hospital.add_patient("Jane Doe")
        self.hospital.discharge_patient("Jane Doe")
        self.assertNotIn("Jane Doe", self.hospital.patients)

    def test_discharge_nonexistent_patient(self):
        with self.assertRaises(ValueError):
            self.hospital.discharge_patient("Nonexistent Patient")

    def test_add_bed(self):
        bed = {'type': 'ICU', 'number': 1}
        self.hospital.add_bed(bed)
        self.assertIn(bed, self.hospital.beds)

    def test_remove_bed(self):
        bed = {'type': 'General', 'number': 2}
        self.hospital.add_bed(bed)
        self.hospital.remove_bed(bed)
        self.assertNotIn(bed, self.hospital.beds)

    def test_remove_nonexistent_bed(self):
        bed = {'type': 'Nonexistent', 'number': 99}
        with self.assertRaises(ValueError):
            self.hospital.remove_bed(bed)

    def test_list_beds_by_type(self):
        bed1 = {'type': 'ICU', 'number': 1}
        bed2 = {'type': 'ICU', 'number': 2}
        bed3 = {'type': 'General', 'number': 3}
        self.hospital.add_bed(bed1)
        self.hospital.add_bed(bed2)
        self.hospital.add_bed(bed3)
        expected = {'ICU': 2, 'General': 1}
        self.assertEqual(self.hospital.list_beds_by_type(), expected)


if __name__ == '__main__':
    unittest.main()
