from enum import Enum

class BedType(Enum):
    REGULAR = "Regular"
    ICU = "ICU"
    EMERGENCY = "Emergency"
    PRIVATE = "Private"

class Bed:
    def __init__(self, bed_id, bed_type=BedType.REGULAR):
        self.bed_id = bed_id
        self.bed_type = bed_type
        self.is_occupied = False
        self.current_patient = None

    def add_patient(self, patient):
        if self.is_occupied:
            raise Exception("Bed is already occupied")
        self.current_patient = patient
        self.is_occupied = True

    def discharge_patient(self):
        if not self.is_occupied:
            raise Exception("Bed is not occupied")
        self.current_patient = None
        self.is_occupied = False

    def update_bed_type(self, new_type):
        if not isinstance(new_type, BedType):
            raise ValueError("new_type must be an instance of BedType")
        self.bed_type = new_type
