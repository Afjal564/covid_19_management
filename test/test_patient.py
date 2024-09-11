import unittest
from unittest.mock import patch, MagicMock
from models.Patient import Patient
import logging

class TestPatient(unittest.TestCase):

    def setUp(self):
        # Mock the database connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cur = self.mock_conn.cursor.return_value
        patch('models.Patient.get_db_connection', return_value=self.mock_conn).start()
        self.addCleanup(patch.stopall)

    def test_initialization(self):
        patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted", assigned_bed="Bed1")
        self.assertEqual(patient.patient_id, "P001")
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.age, 30)
        self.assertEqual(patient.status, "Admitted")
        self.assertEqual(patient.assigned_bed, "Bed1")

    @patch('models.Patient.get_db_connection')
    def test_add_to_db_success(self, mock_get_db_connection):
        patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
        patient.add_to_db()

        self.mock_cur.execute.assert_called_with(
            """
            INSERT INTO patients (patient_id, name, age, status, assigned_bed)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (patient_id) DO UPDATE
            SET name = EXCLUDED.name,
                age = EXCLUDED.age,
                status = EXCLUDED.status,
                assigned_bed = EXCLUDED.assigned_bed;
            """,
            ("P001", "John Doe", 30, "Admitted", None)
        )
        self.mock_conn.commit.assert_called_once()

    @patch('models.Patient.get_db_connection')
    def test_add_to_db_error(self, mock_get_db_connection):
        self.mock_conn.commit.side_effect = Exception("DB error")
        with patch('models.Patient.logging') as mock_logging:
            patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
            patient.add_to_db()
            mock_logging.error.assert_called_with("Error adding patient to database: DB error")

    @patch('models.Patient.get_db_connection')
    def test_discharge_from_db_success(self, mock_get_db_connection):
        patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
        patient.discharge_from_db()

        self.mock_cur.execute.assert_called_with("DELETE FROM patients WHERE patient_id = %s;", ("P001",))
        self.mock_conn.commit.assert_called_once()

    @patch('models.Patient.get_db_connection')
    def test_discharge_from_db_error(self, mock_get_db_connection):
        self.mock_conn.commit.side_effect = Exception("DB error")
        with patch('builtins.print') as mock_print:
            patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
            patient.discharge_from_db()
            mock_print.assert_called_with("Error discharging patient from database: DB error")

    @patch('models.Patient.get_db_connection')
    def test_update_name(self, mock_get_db_connection):
        patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
        with patch.object(patient, 'add_to_db') as mock_add_to_db:
            patient.update_name("Jane Doe")
            self.assertEqual(patient.name, "Jane Doe")
            mock_add_to_db.assert_called_once()

    @patch('models.Patient.get_db_connection')
    def test_update_status(self, mock_get_db_connection):
        patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
        with patch.object(patient, 'add_to_db') as mock_add_to_db:
            patient.update_status("Discharged")
            self.assertEqual(patient.status, "Discharged")
            mock_add_to_db.assert_called_once()

    @patch('models.Patient.get_db_connection')
    def test_update_patient_statistics_admitted(self, mock_get_db_connection):
        Patient.update_patient_statistics("Admitted")
        self.mock_cur.execute.assert_called_with("UPDATE statistics SET total_admitted = total_admitted + 1;")
        self.mock_conn.commit.assert_called_once()

    @patch('models.Patient.get_db_connection')
    def test_update_patient_statistics_discharged(self, mock_get_db_connection):
        Patient.update_patient_statistics("Discharged")
        self.mock_cur.execute.assert_called_with("UPDATE statistics SET total_discharged = total_discharged + 1;")
        self.mock_conn.commit.assert_called_once()

    @patch('models.Patient.get_db_connection')
    def test_update_patient_statistics_invalid_status(self, mock_get_db_connection):
        with patch('builtins.print') as mock_print:
            Patient.update_patient_statistics("InvalidStatus")
            mock_print.assert_called_with("Invalid status: InvalidStatus. No statistics updated.")

    @patch('models.Patient.get_db_connection')
    def test_list_all_admitted_patients(self, mock_get_db_connection):
        self.mock_cur.fetchall.return_value = [
            ("P001", "John Doe", 30, "Admitted", None),
            ("P002", "Jane Smith", 25, "Admitted", "Bed1")
        ]
        patients = Patient.list_all_admitted_patients()
        self.assertEqual(len(patients), 2)
        self.assertEqual(patients[0].patient_id, "P001")
        self.assertEqual(patients[1].name, "Jane Smith")

    @patch('models.Patient.get_db_connection')
    def test_list_all_discharged_patients(self, mock_get_db_connection):
        self.mock_cur.fetchall.return_value = [
            ("P003", "Bob Brown", 45, "Discharged", "Bed2"),
            ("P004", "Alice Green", 50, "Discharged", None)
        ]
        patients = Patient.list_all_discharged_patients()
        self.assertEqual(len(patients), 2)
        self.assertEqual(patients[0].patient_id, "P003")
        self.assertEqual(patients[1].age, 50)

    @patch('models.Patient.get_db_connection')
    def test_list_all_admitted_patients_no_data(self, mock_get_db_connection):
        self.mock_cur.fetchall.return_value = []
        patients = Patient.list_all_admitted_patients()
        self.assertEqual(len(patients), 0)

    @patch('models.Patient.get_db_connection')
    def test_list_all_discharged_patients_no_data(self, mock_get_db_connection):
        self.mock_cur.fetchall.return_value = []
        patients = Patient.list_all_discharged_patients()
        self.assertEqual(len(patients), 0)

    @patch('models.Patient.get_db_connection')
    def test_update_name_with_db_error(self, mock_get_db_connection):
        patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
        with patch.object(patient, 'add_to_db') as mock_add_to_db:
            mock_add_to_db.side_effect = Exception("DB error")
            with self.assertRaises(Exception):
                patient.update_name("Jane Doe")

    @patch('models.Patient.get_db_connection')
    def test_update_status_with_db_error(self, mock_get_db_connection):
        patient = Patient(patient_id="P001", name="John Doe", age=30, status="Admitted")
        with patch.object(patient, 'add_to_db') as mock_add_to_db:
            mock_add_to_db.side_effect = Exception("DB error")
            with self.assertRaises(Exception):
                patient.update_status("Discharged")

    @patch('models.Patient.get_db_connection')
    def test_add_to_db_with_empty_name(self, mock_get_db_connection):
        patient = Patient(patient_id="P002", name="", age=30, status="Admitted")
        patient.add_to_db()
        self.mock_cur.execute.assert_called_with(
            """
            INSERT INTO patients (patient_id, name, age, status, assigned_bed)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (patient_id) DO UPDATE
            SET name = EXCLUDED.name,
                age = EXCLUDED.age,
                status = EXCLUDED.status,
                assigned_bed = EXCLUDED.assigned_bed;
            """,
            ("P002", "", 30, "Admitted", None)
        )

    @patch('models.Patient.get_db_connection')
    def test_discharge_from_db_with_nonexistent_patient(self, mock_get_db_connection):
        # Simulate no rows affected
        self.mock_cur.rowcount = 0
        with patch('builtins.print') as mock_print:
            patient = Patient(patient_id="Nonexistent", name="John Doe", age=30, status="Admitted")
            patient.discharge_from_db()
            mock_print.assert_called_with("No patient found with ID: Nonexistent")

    @patch('models.Patient.get_db_connection')
    def test_add_to_db_with_null_assigned_bed(self, mock_get_db_connection):
        patient = Patient(patient_id="P003", name="Alice Green", age=40, status="Admitted", assigned_bed=None)
        patient.add_to_db()
        self.mock_cur.execute.assert_called_with(
            """
            INSERT INTO patients (patient_id, name, age, status, assigned_bed)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (patient_id) DO UPDATE
            SET name = EXCLUDED.name,
                age = EXCLUDED.age,
                status = EXCLUDED.status,
                assigned_bed = EXCLUDED.assigned_bed;
            """,
            ("P003", "Alice Green", 40, "Admitted", None)
        )

if __name__ == '__main__':
    unittest.main()
