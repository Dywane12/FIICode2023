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
    print(service.get_doctors_nearby_patient(1))


    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")
    """
    Latitude =  47.6472668 
    
    Longitude =  23.552609
    """
    # entering the location name
    getLoc = loc.geocode("Baia mare Garii")

    # printing address
    print(getLoc.address)

    # printing latitude and longitude
    print("Latitude = ", getLoc.latitude, "\n")
    print("Longitude = ", getLoc.longitude)
