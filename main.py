from models.Hospital import Hospital
from models.MunicipalCorporation import MunicipalCorporation
from models.patient import Patient
from models.bed import Bed, BedType

def main_menu():
    print("Who are you?")
    print("1. Hospital")
    print("2. MunicipalCorporation")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        hospital_menu()
    elif choice == "2":
        municipal_corporation_menu()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        main_menu()

def hospital_menu():
    print("Hospital Menu")
    print("1. Add a patient")
    print("2. Discharge a patient")
    print("3. Add a bed")
    print("4. Remove a bed")
    print("5. List beds by type")
    print("6. Go back to main menu")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        name = input("Enter patient name: ")
        age = input("Enter patient age: ")
        status = input("Enter patient status (Admitted/Discharged): ")
        patient = Patient(patient_id="P003", name=name, age=age, status=status)
        hospital.add_patient(patient.name)
        print(f"Patient {name} added.")
    elif choice == "2":
        name = input("Enter patient name to discharge: ")
        hospital.discharge_patient(name)
        print(f"Patient {name} discharged.")
    elif choice == "3":
        bed_id = input("Enter bed ID: ")
        bed_type = input("Enter bed type (Regular, ICU, Emergency, Private): ")
        bed = Bed(bed_id=bed_id, bed_type=BedType[bed_type.upper()])
        hospital.add_bed(bed.__dict__)  # Convert Bed object to dict for compatibility
        print(f"Bed {bed_id} added.")
    elif choice == "4":
        bed_id = input("Enter bed ID to remove: ")
        # In practice, you would need to pass Bed object or modify logic to remove by ID
        # This is simplified for demonstration
        hospital.remove_bed({"id": bed_id})
        print(f"Bed {bed_id} removed.")
    elif choice == "5":
        bed_counts = hospital.list_beds_by_type()
        for bed_type, count in bed_counts.items():
            print(f"Bed Type: {bed_type}, Count: {count}")
    elif choice == "6":
        main_menu()
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
        hospital_menu()

def municipal_corporation_menu():
    print("Municipal Corporation Menu")
    print("1. Add a hospital")
    print("2. Remove a hospital")
    print("3. Update patient statistics")
    print("4. Go back to main menu")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        name = input("Enter hospital name: ")
        pin_code = input("Enter hospital pin code: ")
        hospital = Hospital(name=name, pin_code=pin_code)
        corp.add_hospital(hospital)
        print(f"Hospital {name} added.")
    elif choice == "2":
        name = input("Enter hospital name to remove: ")
        corp.remove_hospital(name)
        print(f"Hospital {name} removed.")
    elif choice == "3":
        admitted = int(input("Enter number of admitted patients: "))
        discharged = int(input("Enter number of discharged patients: "))
        corp.update_patient_statistics(admitted, discharged)
        print(f"Updated statistics. Total admitted: {corp.get_total_admitted_patients()}, Total discharged: {corp.get_total_discharged_patients()}")
    elif choice == "4":
        main_menu()
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
        municipal_corporation_menu()

if __name__ == "__main__":

    global hospital
    global corp
    hospital = Hospital(name="Default Hospital", pin_code="000000")
    corp = MunicipalCorporation(name="Default Corporation")
    main_menu()
