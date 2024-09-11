import psycopg2
from db import get_db_connection
from models.Hospital import Hospital
class MunicipalCorporation:
    def __init__(self, name, corp_id=None):
        self.name = name
        self.corp_id = corp_id
        self.hospitals = self.load_hospitals() if corp_id else []

    def save_to_db(self):
        conn = get_db_connection()
        cur = conn.cursor()
        if self.corp_id:
            cur.execute(
                "UPDATE municipal_corporation SET name=%s WHERE corp_id=%s",
                (self.name, self.corp_id)
            )
        else:
            cur.execute(
                "INSERT INTO municipal_corporation (name) VALUES (%s) RETURNING corp_id",
                (self.name,)
            )
            self.corp_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def load_hospitals(self):
        if not self.corp_id:
            return []
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT hospital_id FROM hospital WHERE corp_id=%s", (self.corp_id,))
        hospital_ids = cur.fetchall()
        cur.close()
        conn.close()
        return [Hospital.fetch_from_db(hospital_id[0]) for hospital_id in hospital_ids]

    def add_hospital(self, hospital):
        if not isinstance(hospital, Hospital):
            raise ValueError("Only Hospital instances can be added.")
        if self.corp_id is None:
            raise ValueError("Municipal Corporation ID is not set.")
        hospital.corp_id = self.corp_id
        hospital.save_to_db()
        self.hospitals.append(hospital)

    def remove_hospital(self, hospital_id):
        hospital = Hospital.fetch_from_db(hospital_id)
        if hospital:
            hospital.remove_from_db()
            self.hospitals = [h for h in self.hospitals if h.hospital_id != hospital_id]
        else:
            raise ValueError("Hospital with ID not found.")

    def edit_hospital(self, hospital_id, new_name=None, new_pin_code=None):
        hospital = Hospital.fetch_from_db(hospital_id)
        if hospital:
            if new_name:
                hospital.name = new_name
            if new_pin_code:
                hospital.pin_code = new_pin_code
            hospital.save_to_db()
        else:
            raise ValueError("Hospital with ID not found.")
