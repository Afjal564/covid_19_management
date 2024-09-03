import unittest
import psycopg2
from models.patient import Patient
from db import get_db_connection

class TestPatient(unittest.TestCase):

    def setUp(self):
        # Set up the database connection and ensure the table exists
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

            # Create the patients table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT,
                age INT,
                status TEXT
            );
        """)
        self.conn.commit()

        # Clean up the table before each test
        self.cursor.execute("TRUNCATE TABLE patients;")
        self.conn.commit()

    def tearDown(self):
        # Clean up and close the database connection after each test
        if not self.conn.closed:
            self.cursor.execute("TRUNCATE TABLE patients;")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def test_add_patient_success(self):
        # Create a test patient
        patient = Patient("123", "John Doe", 30, "Admitted")

        # Add the patient to the database
        patient.add_to_db()

        # Verify the patient was added
        self.cursor.execute("SELECT * FROM patients WHERE patient_id = %s;", ("123",))
        result = self.cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], "John Doe")
        self.assertEqual(result[2], 30)
        self.assertEqual(result[3], "Admitted")

    def test_add_patient_failure(self):
        # Create a test patient
        patient = Patient("123", "John Doe", 30, "Admitted")

        # Intentionally cause a database error by dropping the table
        self.cursor.execute("DROP TABLE patients;")
        self.conn.commit()

        # Attempt to add a patient, expecting failure due to missing table
        with self.assertRaises(psycopg2.Error):
            patient.add_to_db()

        # Recreate the table for future tests
        self.cursor.execute("""
            CREATE TABLE patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT,
                age INT,
                status TEXT
            );
        """)
        self.conn.commit()

    def test_discharge_patient_success(self):
        # First add the patient
        patient = Patient("789", "Alice White", 42, "Admitted")
        patient.add_to_db()

        # Discharge the patient
        patient.discharge_from_db()

        # Verify the patient was discharged (i.e., deleted from the database)
        self.cursor.execute("SELECT * FROM patients WHERE patient_id = %s;", ("789",))
        result = self.cursor.fetchone()

        self.assertIsNone(result)

