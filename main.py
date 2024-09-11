from models.Hospital import Hospital
from models.MunicipalCorporation import MunicipalCorporation
from models.Patient import Patient
from models.bed import Bed, BedType
import unittest
import sys
# main.py
def main_menu():
    print("Who are you?")
    print("1. Hospital")
    print("2. MunicipalCorporation")
    print("3. can you run test cases")
    choice = input("Enter your choice (1 or 2 or 3): ")

    if choice == "1":
        hospital_menu()
    elif choice == "2":
        municipal_corporation_menu()
    elif choice == "3":
        run_test()
    else:
        print("Invalid choice. Please enter 1 or 2.")
        main_menu()


def hospital_menu():
    print("1. Add a patient")
    print("2. Discharge a patient")
    print("3. Add a bed")
    print("4. Remove a bed")
    print("5. List beds by type")
    print("6. Go back to main menu")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        patient_id = input("Enter patient ID: ")
        name = input("Enter patient name: ")
        age = int(input("Enter patient age: "))
        status = input("Enter patient status (Admitted/Discharged): ")
        assigned_bed = input("Enter assigned bed ID (or leave blank): ")
        patient = Patient(patient_id=patient_id, name=name, age=age, status=status, assigned_bed=assigned_bed or None)
        patient.add_to_db()
        print(f"Patient {name} added.")
        Patient.update_patient_statistics(status)
        while True:
            hospitals = input("Back to menu enter 1:  ")
            hospital_menu()

    elif choice == "2":
        patient_id = input("Enter patient ID to discharge: ")
        patient = Patient(patient_id=patient_id, name="", age=0, status="")
        patient.discharge_from_db()
        print(f"Patient with ID {patient_id} discharged.")
        Patient.update_patient_statistics("discharged")
        while True:
            hospitals = input("Back to menu enter 1:  ")
            hospital_menu()

    elif choice == "3":
        bed_id = input("Enter bed ID: ")
        bed_type = input("Enter bed type (Regular, ICU, Emergency, Private): ")
        bed = Bed(bed_id=bed_id, bed_type=BedType[bed_type.upper()])
        bed.add_to_db()
        print(f"Bed {bed_id} added.")
        while True:
            hospitals = input("Back to menu enter 1:  ")
            hospital_menu()

    elif choice == "4":
        bed_id = input("Enter bed ID to remove: ")
        bed = Bed(bed_id=bed_id)
        bed.remove_from_db()
        print(f"Bed {bed_id} removed.")
        while True:
            hospitals = input("Back to menu enter 1:  ")
            hospital_menu()

    elif choice == "5":
        bed_counts = Hospital.list_beds_by_type()
        for bed_type, count in bed_counts.items():
            print(f"Bed Type: {bed_type}, Count: {count}")
        while True:
            hospitals = input("Back to menu enter 1:  ")
            hospital_menu()

    elif choice == "6":
        main_menu()

    else:
        print("Invalid choice. Please enter a number between 1 and 6.")

    hospital_menu()


def get_valid_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def municipal_corporation_menu():
    global corp
    if corp is None:
        print("No valid Municipal Corporation selected.")
        return

    while True:
        print("\nMunicipal Corporation Menu")
        print("1. Add a hospital")
        print("2. Remove a hospital")
        print("3. Edit a hospital")
        print("4. List Hospitals")
        print("5. List Hospitals by pincode")
        print("6. List all Admitted")
        print("7. List all Discharged")
        print("8. Go back to main menu")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            name = input("Enter hospital name: ")
            pin_code = input("Enter hospital pin code: ")
            hospital = Hospital(name=name, pin_code=pin_code, corp_id=corp.corp_id)
            try:
                corp.add_hospital(hospital)
                print(f"Hospital {name} added.")
            except Exception as e:
                print(f"Error adding hospital: {e}")
            while True:
                hospitals = input("Back to menu enter 1:  ")
                municipal_corporation_menu()

        elif choice == "2":
            hospital_id = get_valid_integer("Enter hospital ID to remove: ")
            try:
                corp.remove_hospital(hospital_id)
                print(f"Hospital with ID {hospital_id} removed.")
            except Exception as e:
                print(f"Error removing hospital: {e}")
            while True:
                hospitals = input("Back to menu enter 1:  ")
                municipal_corporation_menu()

        elif choice == "3":
            hospital_id = get_valid_integer("Enter hospital ID to edit: ")
            new_name = input("Enter new hospital name (or leave blank to keep current): ")
            new_pin_code = input("Enter new hospital pin code (or leave blank to keep current): ")
            try:
                corp.edit_hospital(hospital_id, new_name or None, new_pin_code or None)
                print(f"Hospital with ID {hospital_id} updated.")
            except Exception as e:
                print(f"Error updating hospital: {e}")
            while True:
                hospitals = input("Back to menu enter 1:  ")
                municipal_corporation_menu()

        elif choice == "4":
            hospitals = Hospital.list_hospital()
            for hospital in hospitals:
                print(f"Hospital ID: {hospital.hospital_id}, Name: {hospital.name}, Pin Code: {hospital.pin_code}, Corp ID: {hospital.corp_id}")


        elif choice == "5":
            pin_code = input("Enter pin code: ")
            hospitals = Hospital.list_all_hospital_by_pincode(pin_code)
            if not hospitals:
                print(f"No hospitals found for pin code {pin_code}.")
            else:
                for hospital in hospitals:
                    print(f"Name: {hospital.name}, Pin Code: {hospital.pin_code}")
            while True:
                hospitals = input("Back to menu enter 1:  ")
                municipal_corporation_menu()

        elif choice == "6":
            patients = Patient.list_all_admitted_patients()
            if not patients:
                print("No admitted patients found.")
            else:
                for patient in patients:
                    print(f"Patient ID: {patient.patient_id}, Name: {patient.name}, Status: {patient.status}")
            while True:
                hospitals = input("Back to menu enter 1:  ")
                municipal_corporation_menu()

        elif choice == "7":
            patients = Patient.list_all_discharged_patients()  # Call static method directly on the Patient class
            if not patients:
                print("No discharged patients found.")
            else:
                for patient in patients:
                    print(f"Patient ID: {patient.patient_id}, Name: {patient.name}, Status: {patient.status}")
            while True:
                hospitals = input("Back to menu enter 1:  ")
                municipal_corporation_menu()

        elif choice == "8":
            main_menu()
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def run_test():

    test_dir = 'test'

    # Create a test loader and discover tests in the test directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern='test_*.py')

    # Create a test runner and run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with an error code if tests failed
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    # Initialize a default MunicipalCorporation instance
    corp = MunicipalCorporation(name="Default Corporation", corp_id=1)  # Set a valid corp_id here
    # Initialize a default Hospital instance
    hospital = Hospital(name="Default Hospital", pin_code="000000", hospital_id=1)
    main_menu()