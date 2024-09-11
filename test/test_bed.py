import unittest
from unittest.mock import patch, MagicMock
from models.bed import Bed, BedType


class TestBed(unittest.TestCase):

    def setUp(self):
        self.bed = Bed("1", BedType.REGULAR)
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()

    @patch('models.bed.get_db_connection')
    def test_add_to_db_success(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor

        self.bed.add_to_db()

        self.mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO beds (bed_id, bed_type)
            VALUES (%s, %s)
            ON CONFLICT (bed_id) DO UPDATE
            SET bed_type = EXCLUDED.bed_type;
            """, ("1", "Regular")
        )
        self.mock_conn.commit.assert_called_once()
        self.mock_conn.close.assert_called_once()

    @patch('models.bed.get_db_connection')
    def test_add_to_db_error(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_cursor.execute.side_effect = Exception("Database error")

        with self.assertLogs(level='ERROR') as log:
            self.bed.add_to_db()
            self.assertIn("Error adding bed to database: Database error", log.output[0])

        self.mock_conn.close.assert_called_once()

    @patch('models.bed.get_db_connection')
    def test_remove_from_db_success(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor

        self.bed.remove_from_db()

        self.mock_cursor.execute.assert_called_once_with(
            "DELETE FROM beds WHERE bed_id = %s;", ("1",)
        )
        self.mock_conn.commit.assert_called_once()
        self.mock_conn.close.assert_called_once()

    @patch('models.bed.get_db_connection')
    def test_remove_from_db_error(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_cursor.execute.side_effect = Exception("Database error")

        with self.assertLogs(level='ERROR') as log:
            self.bed.remove_from_db()
            self.assertIn("Error removing bed from database: Database error", log.output[0])

        self.mock_conn.close.assert_called_once()

    @patch('models.bed.get_db_connection')
    def test_list_beds_by_type_success(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_cursor.fetchall.return_value = [
            ('Regular', 5),
            ('ICU', 3)
        ]

        result = Bed.list_beds_by_type()

        self.mock_cursor.execute.assert_called_once_with(
            "SELECT bed_type, COUNT(*) FROM beds GROUP BY bed_type;"
        )
        self.assertEqual(result, {'Regular': 5, 'ICU': 3})
        self.mock_conn.close.assert_called_once()

    @patch('models.bed.get_db_connection')
    def test_list_beds_by_type_error(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_cursor.fetchall.side_effect = Exception("Database error")

        result = Bed.list_beds_by_type()

        self.assertEqual(result, {})
        self.mock_conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
