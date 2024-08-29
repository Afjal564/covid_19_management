import unittest
from models.MunicipalCorporation import MunicipalCorporation
class TestMunicipalCorporation(unittest.TestCase):
    def setUp(self):
        # Create an instance of MunicipalCorporation for testing
        self.municipal_corp = MunicipalCorporation("City Corp")

    def test_initialization(self):
        self.assertEqual(self.municipal_corp.name, "City Corp")
        self.assertEqual(self.municipal_corp.hospitals, [])
        self.assertEqual(self.municipal_corp.total_admitted_patients, 0)
        self.assertEqual(self.municipal_corp.total_discharged_patients, 0)


if __name__ == "__main__":
    unittest.main()