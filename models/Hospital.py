
class Hospital:
    def __init__(self, name: str, pin_code: str, beds: list = None, patients: list = None):
        self.name = name
        self.pin_code = pin_code
        self.beds = beds if beds is not None else []
        self.patients = patients if patients is not None else []
        self.add_bed_count = 0
        self.remove_bed_count = 0

    def add_patient(self, patient: str):
        if patient not in self.patients:
            self.patients.append(patient)
        else:
            raise ValueError("Patient already exists in the hospital.")

    def discharge_patient(self, patient: str):
        if patient in self.patients:
            self.patients.remove(patient)
        else:
            raise ValueError("Patient not found in the hospital.")

    def list_beds_by_type(self):
        bed_count_by_type = {}
        for bed in self.beds:
            bed_type = bed.get('type', 'Unknown')
            bed_count_by_type[bed_type] = bed_count_by_type.get(bed_type, 0) + 1
        return bed_count_by_type

    def add_bed(self, bed: dict):
        self.beds.append(bed)
        self.add_bed_count += 1

    def remove_bed(self, bed: dict):
        if bed in self.beds:
            self.beds.remove(bed)
            self.remove_bed_count += 1
        else:
            raise ValueError("Bed not found in the hospital.")
