# models/patient.py

class Patient:
    def __init__(self, patient_id, name, age, status, assigned_bed=None):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.status = status
        self.assigned_bed = assigned_bed

    def __str__(self):
        bed_info = f", Assigned Bed ID: {self.assigned_bed}" if self.assigned_bed else ""
        return (f"Patient ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, "
                f"Status: {self.status}{bed_info}")

    def update_name(self, new_name):
        self.name = new_name

    def update_status(self, new_status):
        self.status = new_status
