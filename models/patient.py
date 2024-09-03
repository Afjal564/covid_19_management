import psycopg2
from db import get_db_connection
import logging



class Patient:
    def __init__(self, patient_id: str, name: str, age: int, status: str, assigned_bed: str = None):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.status = status
        self.assigned_bed = assigned_bed

    def add_to_db(self):
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO patients (patient_id, name, age, status, assigned_bed)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (patient_id) DO UPDATE
                    SET name = EXCLUDED.name,
                        age = EXCLUDED.age,
                        status = EXCLUDED.status,
                        assigned_bed = EXCLUDED.assigned_bed;
                """, (self.patient_id, self.name, self.age, self.status, self.assigned_bed))
                conn.commit()
        except Exception as e:
            logging.error(f"Error adding patient to database: {e}")
        finally:
            conn.close()
    def discharge_from_db(self):
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM patients WHERE patient_id = %s;", (self.patient_id,))
                conn.commit()
        except Exception as e:
            print(f"Error discharging patient from database: {e}")
        finally:
            conn.close()

    def update_name(self, new_name: str):
        self.name = new_name
        self.add_to_db()

    def update_status(self, new_status: str):
        self.status = new_status
        self.add_to_db()

    @staticmethod
    def update_patient_statistics(status: str):
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                if status.lower() == "admitted":
                    cur.execute("UPDATE statistics SET total_admitted = total_admitted + 1;")
                elif status.lower() == "discharged":
                    cur.execute("UPDATE statistics SET total_discharged = total_discharged + 1;")
                else:
                    print(f"Invalid status: {status}. No statistics updated.")
                    return
                conn.commit()
        except Exception as e:
            print(f"Error updating patient statistics: {e}")
        finally:
            conn.close()

    @staticmethod
    def list_all_admitted_patients():
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                # Fetch all patients with status 'Admitted'
                cur.execute("SELECT patient_id, name, age, status, assigned_bed FROM patients WHERE status = %s;", ('Admitted',))
                results = cur.fetchall()
                # Create Patient objects for each result
                patients = [Patient(patient_id=row[0], name=row[1], age=row[2], status=row[3], assigned_bed=row[4]) for row in results]
                return patients
        except Exception as e:
            print(f"Error retrieving admitted patients: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def list_all_discharged_patients():
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                # Fetch all patients with status 'Discharged'
                cur.execute("SELECT patient_id, name, age, status, assigned_bed FROM patients WHERE status = %s;", ('Discharged',))
                results = cur.fetchall()
                # Create Patient objects for each result
                patients = [Patient(patient_id=row[0], name=row[1], age=row[2], status=row[3], assigned_bed=row[4]) for row in results]
                return patients
        except Exception as e:
            print(f"Error retrieving discharged patients: {e}")
            return []
        finally:
            conn.close()
