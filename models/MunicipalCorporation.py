class MunicipalCorporation:
    def __init__(self, name: str):
        self.name = name
        self.hospitals = []
        self.total_admitted_patients = 0
        self.total_discharged_patients = 0

    def add_hospital(self, hospital):
        if hospital not in self.hospitals:
            self.hospitals.append(hospital)
        else:
            raise ValueError("Hospital already exists in the municipal corporation.")

    def remove_hospital(self, hospital_name: str):
        for hospital in self.hospitals:
            if hospital.name == hospital_name:
                self.hospitals.remove(hospital)
                return
        raise ValueError("Hospital not found in the municipal corporation.")

    def get_total_admitted_patients(self) -> int:
        return self.total_admitted_patients

    def get_total_discharged_patients(self) -> int:
        return self.total_discharged_patients

    def update_patient_statistics(self, admitted: int, discharged: int):
        self.total_admitted_patients += admitted
        self.total_discharged_patients += discharged
