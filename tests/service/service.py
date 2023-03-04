from app import db
from app.repository.database import Database
from app.domain.entities import Doctor, Consultation, Patient
from app import app
from app.service.service import Service

with app.app_context():
    db_1 = Database(db)
    service = Service(db_1)
    #doctor = db.session.get(Doctor, 10000)
    #patients = service.get_doctor_patients(doctor)
    patient = db.session.get(Patient, 21)
    consultation_history = service.get_patient_consultation(patient)
    print(consultation_history)
