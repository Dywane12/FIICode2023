from datetime import datetime

from app import db
from app.repository.database import Database
from app.domain.entities import Doctor, Consultation, Patient, InviteCode
from app import app
from app.service.service import Service
from flask import session
import os
with app.app_context():
    db_1 = Database(db)
    service = Service(db_1, session)
    ok = db_1.find_invite_code(1234567)
    print(ok)
