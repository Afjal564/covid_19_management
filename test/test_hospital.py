import unittest
from unittest.mock import patch, MagicMock
from models.Hospital import Hospital  # Ensure this path is correct

class TestHospital(unittest.TestCase):

    @patch('models.Hospital.get_db_connection')  # Ensure this path matches the actual path in your project
    def test_save_to_db_insert(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Test inserting a new Hospital
        hospital_instance = Hospital(name="City Hospital", pin_code="12345")
        mock_cursor.fetchone.return_value = (1,)  # Simulate returning a new hospital_id

        hospital_instance.save_to_db()

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO hospital (name, pin_code, corp_id) VALUES (%s, %s, %s) RETURNING hospital_id",
            ("City Hospital", "12345", None)
        )
        self.assertEqual(hospital_instance.hospital_id, 1)
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('models.Hospital.get_db_connection')
    def test_save_to_db_update(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Test updating an existing Hospital
        hospital_instance = Hospital(name="City Hospital", pin_code="12345", hospital_id=1, corp_id=10)

        hospital_instance.save_to_db()

        mock_cursor.execute.assert_called_once_with(
            "UPDATE hospital SET name=%s, pin_code=%s, corp_id=%s WHERE hospital_id=%s",
            ("City Hospital", "12345", 10, 1)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('models.Hospital.get_db_connection')
    def test_remove_from_db(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Test removing an existing Hospital
        hospital_instance = Hospital(name="City Hospital", pin_code="12345", hospital_id=1)
        hospital_instance.remove_from_db()

        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM hospitals WHERE hospital_id=%s",
            (1,)
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('models.Hospital.get_db_connection')
    def test_remove_from_db_no_id(self, mock_get_db_connection):
        # Test removing a Hospital without a hospital_id
        hospital_instance = Hospital(name="City Hospital", pin_code="12345")
        with self.assertRaises(ValueError) as context:
            hospital_instance.remove_from_db()
        self.assertEqual(str(context.exception), "Hospital ID is required to remove the hospital.")

    @patch('models.Hospital.get_db_connection')
    def test_fetch_from_db(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Test fetching an existing Hospital
        mock_cursor.fetchone.return_value = (1, "City Hospital", "12345", 10)
        hospital_instance = Hospital.fetch_from_db(1)

        self.assertIsNotNone(hospital_instance)
        self.assertEqual(hospital_instance.hospital_id, 1)
        self.assertEqual(hospital_instance.name, "City Hospital")
        self.assertEqual(hospital_instance.pin_code, "12345")
        self.assertEqual(hospital_instance.corp_id, 10)

    @patch('models.Hospital.get_db_connection')
    def test_fetch_from_db_not_found(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        # Test fetching a non-existent Hospital
        mock_cursor.fetchone.return_value = None
        hospital_instance = Hospital.fetch_from_db(999)

        self.assertIsNone(hospital_instance)

if __name__ == '__main__':
    unittest.main()
