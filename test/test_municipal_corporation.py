import unittest

from models.Hospital import Hospital
from models.MunicipalCorporation import MunicipalCorporation


class TestMunicipalCorporation(unittest.TestCase):
    def setUp(self):
        self.corporation = MunicipalCorporation(name="Metro Corp")
        self.hospital1 = Hospital(name="City Hospital", pin_code="12345")
        self.hospital2 = Hospital(name="Green Hospital", pin_code="67890")

    def test_add_hospital(self):
        self.corporation.add_hospital(self.hospital1)
        self.assertIn(self.hospital1, self.corporation.hospitals)

    def test_add_duplicate_hospital(self):
        self.corporation.add_hospital(self.hospital1)
        with self.assertRaises(ValueError):
            self.corporation.add_hospital(self.hospital1)

    def test_remove_hospital(self):
        self.corporation.add_hospital(self.hospital1)
        self.corporation.remove_hospital("City Hospital")
        self.assertNotIn(self.hospital1, self.corporation.hospitals)

    def test_remove_nonexistent_hospital(self):
        with self.assertRaises(ValueError):
            self.corporation.remove_hospital("Nonexistent Hospital")

    def test_update_patient_statistics(self):
        self.corporation.update_patient_statistics(admitted=10, discharged=5)
        self.assertEqual(self.corporation.get_total_admitted_patients(), 10)
        self.assertEqual(self.corporation.get_total_discharged_patients(), 5)

        self.corporation.update_patient_statistics(admitted=3, discharged=2)
        self.assertEqual(self.corporation.get_total_admitted_patients(), 13)
        self.assertEqual(self.corporation.get_total_discharged_patients(), 7)


if __name__ == '__main__':
    unittest.main()
