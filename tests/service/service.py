from datetime import datetime

from app import db
from app.repository.database import Database
from app.domain.entities import Doctor, Consultation, Patient
from app import app
from app.service.service import Service
from flask import session
import os
with app.app_context():
    db_1 = Database(db)
    service = Service(db_1, session)


    print(OK)
