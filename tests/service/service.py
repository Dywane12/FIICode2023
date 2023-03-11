
from app import db
from app.repository.database import Database
from app.domain.entities import Doctor, Consultation, Patient
from app import app
from app.service.service import Service
from flask import session

with app.app_context():
    db_1 = Database(db)
    service = Service(db_1, session)
    #doctor = db.session.get(Doctor, 10000)
    #patients = service.get_doctor_patients(doctor)
    patient = db.session.get(Patient, 21)
    print(service.get_doctor_by_username(patient.username))
    print(service.get_patient_by_username(patient.username))
