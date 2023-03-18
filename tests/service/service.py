
from app import db
from app.repository.database import Database
from app.domain.entities import Doctor, Consultation, Patient
from app import app
from app.service.service import Service
from flask import session

with app.app_context():
    db_1 = Database(db)
    service = Service(db_1, session)
    OK = service.validate_medical_proof('Medical+degree.pdf','CALIN ANDREI')
    print(OK)
