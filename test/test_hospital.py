import unittest
from unittest.mock import patch, MagicMock
from models.Hospital import Hospital
import psycopg2

class TestHospital(unittest.TestCase):

    @patch('models.Hospital.get_db_connection')
    def test_save_to_db_insert(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchone.return_value = [1]
        mock_get_db_connection.return_value = mock_conn

        hospital = Hospital(name="Test Hospital", pin_code="123456", corp_id=1)
        hospital.save_to_db()

        mock_cur.execute.assert_called_with(
            "INSERT INTO hospital (name, pin_code, corp_id) VALUES (%s, %s, %s) RETURNING hospital_id",
            ("Test Hospital", "123456", 1)
        )
        self.assertEqual(hospital.hospital_id, 1)

    @patch('models.Hospital.get_db_connection')
    def test_save_to_db_update(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        hospital = Hospital(name="Test Hospital", pin_code="123456", hospital_id=1, corp_id=1)
        hospital.save_to_db()

        mock_conn.cursor.return_value.execute.assert_called_with(
            "UPDATE hospital SET name=%s, pin_code=%s, corp_id=%s WHERE hospital_id=%s",
            ("Test Hospital", "123456", 1, 1)
        )

    @patch('models.Hospital.get_db_connection')
    def test_save_to_db_error(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.execute.side_effect = psycopg2.Error("Database error")
        mock_get_db_connection.return_value = mock_conn

        hospital = Hospital(name="Test Hospital", pin_code="123456", corp_id=1)
        hospital.save_to_db()

        mock_cur.execute.assert_called()
        self.assertLogs(level='INFO')

    @patch('models.Hospital.get_db_connection')
    def test_remove_from_db(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        hospital = Hospital(name="Test Hospital", pin_code="123456", hospital_id=1)
        hospital.remove_from_db()

        mock_conn.cursor.return_value.execute.assert_called_with(
            "DELETE FROM hospital WHERE hospital_id=%s",
            (1,)
        )

    @patch('models.Hospital.get_db_connection')
    def test_remove_from_db_error(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.execute.side_effect = psycopg2.Error("Database error")
        mock_get_db_connection.return_value = mock_conn

        hospital = Hospital(name="Test Hospital", pin_code="123456", hospital_id=1)
        hospital.remove_from_db()

        mock_cur.execute.assert_called()
        self.assertLogs(level='INFO')

    @patch('models.Hospital.get_db_connection')
    def test_remove_from_db_no_id(self, mock_get_db_connection):
        hospital = Hospital(name="Test Hospital", pin_code="123456")
        with self.assertRaises(ValueError):
            hospital.remove_from_db()

    @patch('models.Hospital.get_db_connection')
    def test_list_hospital(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = [(1, "Test Hospital", "123456", 1)]
        mock_get_db_connection.return_value = mock_conn

        hospitals = Hospital.list_hospital()

        self.assertEqual(len(hospitals), 1)
        self.assertEqual(hospitals[0].name, "Test Hospital")

    @patch('models.Hospital.get_db_connection')
    def test_list_hospital_empty(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = []
        mock_get_db_connection.return_value = mock_conn

        hospitals = Hospital.list_hospital()

        self.assertEqual(len(hospitals), 0)

    @patch('models.Hospital.get_db_connection')
    def test_list_all_hospital_by_pincode(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = [("Test Hospital", "123456")]
        mock_get_db_connection.return_value = mock_conn

        hospitals = Hospital.list_all_hospital_by_pincode("123456")

        self.assertEqual(len(hospitals), 1)
        self.assertEqual(hospitals[0].name, "Test Hospital")

    @patch('models.Hospital.get_db_connection')
    def test_list_all_hospital_by_pincode_empty(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = []
        mock_get_db_connection.return_value = mock_conn

        hospitals = Hospital.list_all_hospital_by_pincode("123456")

        self.assertEqual(len(hospitals), 0)

    @patch('models.Hospital.get_db_connection')
    def test_list_beds_by_type(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = [("ICU", 5), ("General", 10)]
        mock_get_db_connection.return_value = mock_conn

        bed_counts = Hospital.list_beds_by_type()

        self.assertEqual(bed_counts['ICU'], 5)
        self.assertEqual(bed_counts['General'], 10)

    @patch('models.Hospital.get_db_connection')
    def test_list_beds_by_type_empty(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = []
        mock_get_db_connection.return_value = mock_conn

        bed_counts = Hospital.list_beds_by_type()

        self.assertEqual(len(bed_counts), 0)

    @patch('models.Hospital.get_db_connection')
    def test_fetch_from_db(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchone.return_value = (1, "Test Hospital", "123456", 1)
        mock_get_db_connection.return_value = mock_conn

        hospital = Hospital.fetch_from_db(1)

        self.assertIsNotNone(hospital)
        self.assertEqual(hospital.name, "Test Hospital")

    @patch('models.Hospital.get_db_connection')
    def test_fetch_from_db_no_result(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchone.return_value = None
        mock_get_db_connection.return_value = mock_conn

        hospital = Hospital.fetch_from_db(1)

        self.assertIsNone(hospital)

if __name__ == '__main__':
    unittest.main()
