import psycopg2
from db import get_db_connection

class Hospital:
    def __init__(self, name, pin_code, hospital_id=None, corp_id=None):
        self.name = name
        self.pin_code = pin_code
        self.hospital_id = hospital_id
        self.corp_id = corp_id

    def save_to_db(self):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if self.hospital_id:
                # Update existing hospital
                cur.execute(
                    "UPDATE hospital SET name=%s, pin_code=%s, corp_id=%s WHERE hospital_id=%s",
                    (self.name, self.pin_code, self.corp_id, self.hospital_id)
                )
            else:
                # Insert new hospital
                cur.execute(
                    "INSERT INTO hospital (name, pin_code, corp_id) VALUES (%s, %s, %s) RETURNING hospital_id",
                    (self.name, self.pin_code, self.corp_id)
                )
                self.hospital_id = cur.fetchone()[0]
            conn.commit()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
        finally:
            cur.close()
            conn.close()

    def remove_from_db(self):
        if not self.hospital_id:
            raise ValueError("Hospital ID is required to remove the hospital.")
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM hospital WHERE hospital_id=%s",
                (self.hospital_id,)
            )
            conn.commit()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def list_beds_by_type():
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT bed_type, COUNT(*) FROM beds GROUP BY bed_type;")
                results = cur.fetchall()
                bed_counts = {row[0]: row[1] for row in results}
            return bed_counts
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return {}
        finally:
            conn.close()

    @staticmethod
    def list_hospital():
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT hospital_id, name, pin_code, corp_id FROM hospital")
                results = cur.fetchall()
                hospitals = [Hospital(hospital_id=row[0], name=row[1], pin_code=row[2], corp_id=row[3]) for row in results]
            return hospitals
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def list_all_hospital_by_pincode(pin_code):
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT name, pin_code FROM hospital WHERE pin_code = %s", (pin_code,))
                results = cur.fetchall()
                hospitals = [Hospital(name=row[0], pin_code=row[1]) for row in results]
                return hospitals
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def fetch_from_db(hospital_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT hospital_id, name, pin_code, corp_id FROM hospital WHERE hospital_id=%s",
                (hospital_id,)
            )
            row = cur.fetchone()
            if row:
                return Hospital(name=row[1], pin_code=row[2], hospital_id=row[0], corp_id=row[3])
            else:
                return None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            cur.close()
            conn.close()
