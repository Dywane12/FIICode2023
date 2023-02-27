from app import db
from datetime import datetime


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), index=True,  nullable=False)
    last_name = db.Column(db.String(64), index=True,  nullable=False)
    phone_number = db.Column(db.Integer, index=True, unique=True,  nullable=False)
    email = db.Column(db.String(128), index=True, unique=True,  nullable=False)
    address = db.Column(db.String(256), index=True,  nullable=False)
    id_series = db.Column(db.String(8), index=True, unique=True, nullable=False)
    id_number = db.Column(db.String(16), index=True, unique=True, nullable=False)
    cnp = db.Column(db.Integer, index=True, unique=True,  nullable=False)
    birth_date = db.Column(db.String(128), index=True,  nullable=False)
    marital_status = db.Column(db.String(16), index=True,  nullable=False)
    gender = db.Column(db.String(8), index=True, nullable=False)
    medical_record_id = db.Column(db.Integer, index=True, unique=True,  nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'),  nullable=False)
    consultation = db.relationship('Consultation', backref='patient', lazy='dynamic')

    def __init__(self, username, first_name, last_name, phone_number, email, address, id_series, id_number, cnp,
                 birth_date, marital_status, gender, medical_record_id, doctor_id):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.id_series = id_series
        self.id_number = id_number
        self.cnp = cnp
        self.birth_date = birth_date
        self.marital_status = marital_status
        self.gender = gender
        self.medical_record_id = medical_record_id
        self.doctor_id = doctor_id


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    phone_number = db.Column(db.Integer, index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    address = db.Column(db.String(256), index=True, nullable=False)
    birth_date = db.Column(db.String(128), index=True, nullable=False)
    gender = db.Column(db.String(8), index=True, nullable=False)
    consultation_schedule_office = db.Column(db.String(128), index=True, nullable=False)
    consultation_schedule_away = db.Column(db.String(128), index=True, nullable=False)
    assistants_schedule = db.Column(db.String(128), index=True)
    patients = db.relationship('Patient', backref='doctor', lazy='dynamic')
    consultations = db.relationship('Consultation', backref='doctor', lazy='dynamic')

    def __init__(self, username,  first_name, last_name, phone_number, email, address, birth_date,
                 gender, consultation_schedule_office, consultation_schedule_away, assistants_schedule):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birth_date = birth_date
        self.gender = gender
        self.consultation_schedule_office = consultation_schedule_office
        self.consultation_schedule_away = consultation_schedule_away
        self.assistants_schedule = assistants_schedule

    def __repr__(self):
        return f'doctor: {self.username}'


class Consultation(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    time = db.Column(db.String(128), index=True, unique=True, nullable=False)

    def __init__(self, patient_id, doctor_id, time):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.time = time