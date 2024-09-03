import unittest
from unittest.mock import patch, MagicMock
from models.bed import Bed, BedType, get_db_connection

class TestBed(unittest.TestCase):

    # @patch('models.bed.get_db_connection')
    # def test_add_to_db(self, mock_get_db_connection):
    #     mock_conn = MagicMock()
    #     mock_cursor = MagicMock()
    #     mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    #     mock_get_db_connection.return_value = mock_conn
    #
    #     bed = Bed("001", BedType.REGULAR)
    #     bed.add_to_db()
    #
    #     mock_cursor.execute.assert_called_once_with("""
    #         INSERT INTO beds (bed_id, bed_type)
    #         VALUES (%s, %s)
    #         ON CONFLICT (bed_id) DO UPDATE
    #         SET bed_type = EXCLUDED.bed_type;
    #     """, ("001", "Regular"))
    #     mock_conn.commit.assert_called_once()
    #     mock_conn.close.assert_called_once()

    @patch('models.bed.get_db_connection')
    def test_remove_from_db(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        bed = Bed("001", BedType.REGULAR)
        bed.remove_from_db()

        mock_cursor.execute.assert_called_once_with("DELETE FROM beds WHERE bed_id = %s;", ("001",))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('models.bed.get_db_connection')
    def test_list_beds_by_type(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_conn

        mock_cursor.fetchall.return_value = [
            ('Regular', 10),
            ('ICU', 5)
        ]

        bed_counts = Bed.list_beds_by_type()

        self.assertEqual(bed_counts, {
            'Regular': 10,
            'ICU': 5
        })
        mock_cursor.execute.assert_called_once_with("SELECT bed_type, COUNT(*) FROM beds GROUP BY bed_type;")
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
