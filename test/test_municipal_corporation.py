import unittest
from unittest.mock import patch, MagicMock
from models.MunicipalCorporation import MunicipalCorporation
from models.Hospital import Hospital


class TestMunicipalCorporation(unittest.TestCase):

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_save_new_corporation(self, mock_get_db_connection):
        # Setup mock
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchone.return_value = [1]  # Simulate returning a new corp_id
        mock_get_db_connection.return_value = mock_conn

        # Test new municipal corporation save
        corp = MunicipalCorporation(name="Test Corporation")
        corp.save_to_db()

        self.assertEqual(corp.corp_id, 1)
        mock_cur.execute.assert_called_with(
            "INSERT INTO municipal_corporation (name) VALUES (%s) RETURNING corp_id",
            ("Test Corporation",)
        )
        mock_conn.commit.assert_called_once()

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_update_corporation(self, mock_get_db_connection):
        # Setup mock
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Test updating an existing municipal corporation
        corp = MunicipalCorporation(name="Updated Corporation", corp_id=1)
        corp.save_to_db()

        mock_conn.cursor.return_value.execute.assert_called_with(
            "UPDATE municipal_corporation SET name=%s WHERE corp_id=%s",
            ("Updated Corporation", 1)
        )
        mock_conn.commit.assert_called_once()

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_load_hospitals(self, mock_get_db_connection):
        # Setup mock for loading hospitals
        mock_conn = MagicMock()
        mock_cur = mock_conn.cursor.return_value
        mock_cur.fetchall.return_value = [(1,), (2,)]  # Simulate hospital IDs
        mock_get_db_connection.return_value = mock_conn

        with patch('models.Hospital.Hospital.fetch_from_db') as mock_fetch_hospital:
            mock_fetch_hospital.side_effect = [Hospital(name="Hospital 1", hospital_id=1),
                                               Hospital(name="Hospital 2", hospital_id=2)]

            corp = MunicipalCorporation(name="Corp", corp_id=1)
            hospitals = corp.load_hospitals()

            self.assertEqual(len(hospitals), 2)
            mock_fetch_hospital.assert_any_call(1)
            mock_fetch_hospital.assert_any_call(2)

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_add_hospital(self, mock_get_db_connection):
        # Setup mock
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Test adding a hospital
        corp = MunicipalCorporation(name="Corp", corp_id=1)
        hospital = Hospital(name="New Hospital", pin_code="123456")
        with patch.object(Hospital, 'save_to_db') as mock_save_to_db:
            corp.add_hospital(hospital)
            mock_save_to_db.assert_called_once()
            self.assertEqual(hospital.corp_id, 1)
            self.assertEqual(len(corp.hospitals), 1)

    def test_add_invalid_hospital(self):
        corp = MunicipalCorporation(name="Corp", corp_id=1)
        with self.assertRaises(ValueError):
            corp.add_hospital("invalid_hospital")

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_remove_hospital(self, mock_get_db_connection):
        # Setup mock
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        with patch.object(Hospital, 'fetch_from_db') as mock_fetch_hospital:
            mock_fetch_hospital.return_value = Hospital(name="Hospital 1", hospital_id=1)
            with patch.object(Hospital, 'remove_from_db') as mock_remove_from_db:
                corp = MunicipalCorporation(name="Corp", corp_id=1)
                corp.hospitals = [Hospital(name="Hospital 1", hospital_id=1)]
                corp.remove_hospital(1)

                mock_remove_from_db.assert_called_once()
                self.assertEqual(len(corp.hospitals), 0)

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_remove_nonexistent_hospital(self, mock_get_db_connection):
        # Setup mock
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        with patch.object(Hospital, 'fetch_from_db') as mock_fetch_hospital:
            mock_fetch_hospital.return_value = None  # Hospital not found
            corp = MunicipalCorporation(name="Corp", corp_id=1)
            with self.assertRaises(ValueError):
                corp.remove_hospital(99)

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_edit_hospital(self, mock_get_db_connection):
        # Setup mock
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        with patch.object(Hospital, 'fetch_from_db') as mock_fetch_hospital:
            hospital = Hospital(name="Hospital 1", hospital_id=1)
            mock_fetch_hospital.return_value = hospital

            with patch.object(Hospital, 'save_to_db') as mock_save_to_db:
                corp = MunicipalCorporation(name="Corp", corp_id=1)
                corp.edit_hospital(1, new_name="Updated Hospital", new_pin_code="654321")

                self.assertEqual(hospital.name, "Updated Hospital")
                self.assertEqual(hospital.pin_code, "654321")
                mock_save_to_db.assert_called_once()

    @patch('models.MunicipalCorporation.get_db_connection')
    def test_edit_nonexistent_hospital(self, mock_get_db_connection):
        # Setup mock
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        with patch.object(Hospital, 'fetch_from_db') as mock_fetch_hospital:
            mock_fetch_hospital.return_value = None  # Hospital not found

            corp = MunicipalCorporation(name="Corp", corp_id=1)
            with self.assertRaises(ValueError):
                corp.edit_hospital(99, new_name="Updated Hospital", new_pin_code="654321")


if __name__ == '__main__':
    unittest.main()
