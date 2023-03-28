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
    print(os.path.abspath(os.path.join(app.root_path, 'static/files', 'consultation',
                                   '1.pdf')))
