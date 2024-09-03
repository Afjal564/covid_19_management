import psycopg2
from db import get_db_connection
from enum import Enum

class BedType(Enum):
    REGULAR = "Regular"
    ICU = "ICU"
    EMERGENCY = "Emergency"
    PRIVATE = "Private"

class Bed:
    def __init__(self, bed_id: str, bed_type: BedType):
        self.bed_id = bed_id
        self.bed_type = bed_type

    def add_to_db(self):
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO beds (bed_id, bed_type)
                    VALUES (%s, %s)
                    ON CONFLICT (bed_id) DO UPDATE
                    SET bed_type = EXCLUDED.bed_type;
                """, (self.bed_id, self.bed_type.value))
                conn.commit()
        except Exception as e:
            print(f"Error adding bed to database: {e}")
        finally:
            conn.close()

    def remove_from_db(self):
        global conn
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM beds WHERE bed_id = %s;", (self.bed_id,))
                conn.commit()
        except Exception as e:
            print(f"Error removing bed from database: {e}")
        finally:
            conn.close()

    @staticmethod
    def list_beds_by_type():
        global conn
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT bed_type, COUNT(*) FROM beds GROUP BY bed_type;")
                results = cur.fetchall()
                bed_counts = {row[0]: row[1] for row in results}
            return bed_counts
        except Exception as e:
            print(f"Error retrieving bed counts: {e}")
            return {}
        finally:
            conn.close()
