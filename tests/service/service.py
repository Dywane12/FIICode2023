from datetime import datetime

import os
from app import app

FOLDER = os.path.abspath(os.path.join(app.root_path, 'static/files'))
from geopy.geocoders import Nominatim
from app import db
from app.repository.database import Database
from app.domain.entities import Doctor, Consultation, Patient, InviteCode
from app.service.service import Service
from flask import session

with app.app_context():
    db_1 = Database(db)
    service = Service(db_1, session)
    patient = service.get_patient_by_id(1)
    information_sheet = service.get_information_sheet_by_patient_id(patient.id)
    print(information_sheet.medical_history)
