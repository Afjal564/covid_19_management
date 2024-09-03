CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    status VARCHAR(50),
    assigned_bed INTEGER
);

CREATE TABLE hospitals (
    hospital_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    pin_code VARCHAR(10)
);

CREATE TABLE beds (
    bed_id SERIAL PRIMARY KEY,
    bed_type VARCHAR(50),
    is_occupied BOOLEAN,
    current_patient INTEGER
);

CREATE TABLE municipal_corporations (
    corp_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
