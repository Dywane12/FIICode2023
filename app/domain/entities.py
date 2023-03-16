from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login_manager
from hashlib import md5


class Patient(UserMixin, db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.Integer, index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    address = db.Column(db.String(256), index=True)
    postalcode = db.Column(db.String(256), index=True )
    city = db.Column(db.String(256), index=True)
    state = db.Column(db.String(256), index=True)
    passport_id = db.Column(db.String(16), index=True, unique=True)
    birth_date = db.Column(db.String(128), index=True)
    marital_status = db.Column(db.String(16), index=True)
    gender = db.Column(db.String(8), index=True)
    occupation = db.Column(db.String(256), index=True)
    password_hash = db.Column(db.String(256), index=True, unique=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    consultations = db.relationship('Consultation', backref='patient')
    information_sheet = db.relationship('InformationSheet', backref='patient')

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None,
                 city=None, state=None, postalcode=None, passport_id=None,
                 birth_date=None, marital_status=None, gender=None, occupation=None, medical_record_id=None,
                 doctor_id=None, password_hash=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.postalcode = postalcode
        self.passport_id = passport_id
        self.birth_date = birth_date
        self.marital_status = marital_status
        self.gender = gender
        self.occupation = occupation
        self.medical_record_id = medical_record_id
        self.password_hash = password_hash
        self.doctor_id = doctor_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return f'Patient: {self.username}'

    def __str__(self):
        return f'Patient: {self.username}'


class Doctor(UserMixin, db.Model):
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.Integer, index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    address = db.Column(db.String(256), index=True)
    postalcode = db.Column(db.String(256), index=True)
    city = db.Column(db.String(256), index=True)
    state = db.Column(db.String(256), index=True)
    birth_date = db.Column(db.String(128), index=True)
    gender = db.Column(db.String(8), index=True)
    consultation_schedule_office = db.Column(db.String(128), index=True)
    consultation_schedule_away = db.Column(db.String(128), index=True)
    assistants_schedule = db.Column(db.String(128), index=True)
    password_hash = db.Column(db.String(256), index=True)
    patients = db.relationship('Patient', backref='doctor')
    consultations = db.relationship('Consultation', backref='doctor')

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None,
                 city=None, state=None, postalcode=None,
                 birth_date=None,
                 gender=None, consultation_schedule_office=None, consultation_schedule_away=None,
                 assistants_schedule=None, password_hash=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.postalcode = postalcode
        self.birth_date = birth_date
        self.gender = gender
        self.consultation_schedule_office = consultation_schedule_office
        self.consultation_schedule_away = consultation_schedule_away
        self.assistants_schedule = assistants_schedule
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return f'doctor: {self.username}'

    def __str__(self):
        return f'doctor: {self.username}'


@login_manager.user_loader
def load_user(id):
    return Doctor.query.get(int(id))


class Consultation(db.Model):
    __tablename__ = "consultation"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'),)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    time = db.Column(db.Date, index=True)
    pdf = db.Column(db.String(128))
    urgency_grade = db.Column(db.String(128),index=True)

    def __init__(self, patient_id=None, doctor_id=None, time=None, pdf=None, urgency_grade=None):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.time = time
        self.pdf = pdf
        self.urgency_grade = urgency_grade


information_sheet_chronic_disease = db.Table('information_sheet_chronic_disease',
                                             db.Column('patient_id', db.Integer,
                                                       db.ForeignKey('information_sheet.patient_id')),
                                             db.Column('chronic_disease_id', db.Integer,
                                                       db.ForeignKey('chronic_disease.id'))
                                             )

information_sheet_allergy = db.Table('information_sheet_allergy',
                                     db.Column('patient_id', db.Integer, db.ForeignKey('information_sheet.patient_id')),
                                     db.Column('allergy_id', db.Integer, db.ForeignKey('allergy.id'))
                                     )


class InformationSheet(db.Model):
    __tablename__ = "information_sheet"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    weight = db.Column(db.Integer, index=True)
    height = db.Column(db.Integer, index=True)
    shoe_size = db.Column(db.Integer, index=True)
    blood_type = db.Column(db.String(256), index=True)
    medical_history = db.relationship('ChronicDisease', secondary=information_sheet_chronic_disease, backref='patients')
    medications = db.relationship('Drug', backref='patient')
    allergies = db.relationship('Allergy', secondary=information_sheet_allergy, backref='patients')
    hospitalization = db.relationship('Hospitalization', backref='patient')
    smoking = db.relationship('Smoker', backref='patient')
    drinking = db.relationship('Drinker', backref='patient')
    family_history = db.relationship('FamilyHistory', backref='patient')

    def init(self, patient_id=None, weigth=None, height=None, shoe_size=None, blood_type=None):
        self.patient_id = patient_id
        self.weight = weigth
        self.height = height
        self.shoe_size = shoe_size
        self.blood_type = blood_type


class ChronicDisease(db.Model):
    __tablename__ = "chronic_disease"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)


class Drug(db.Model):
    __tablename__ = "drug"
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'), primary_key=True)
    name = db.Column(db.String(256), index=True)
    dosage = db.Column(db.String(256))
    frequency = db.Column(db.String(256))


class Allergy(db.Model):
    __tablename__ = "allergy"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)


class Hospitalization(db.Model):
    __tablename__ = "hospitalization"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'))
    date = db.Column(db.Date)
    reason = db.Column(db.String(500))


class Smoker(db.Model):
    __tablename__ = "smoker"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'))
    current_packs_per_day = db.Column(db.Integer, nullable=True)
    previous_pack_per_day = db.Column(db.Integer, nullable=True)
    smoking_years = db.Column(db.Integer, nullable=True)

    def __init__(self, current_packs_per_day=None, previous_pack_per_day=None, smoking_years=None):
        self.current_packs_per_day = current_packs_per_day
        self.previous_pack_per_day = previous_pack_per_day
        self.smoking_years = smoking_years


class Drinker(db.Model):
    __tablename__ = "drinker"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'))
    quantity = db.Column(db.Integer, nullable=True)
    frequency = db.Column(db.Integer, nullable=True)

    def __init__(self, quantity, frequency):
        self.quantity = quantity
        self.frequency = frequency


class Mother(db.Model):
    __tablename__ = "mother"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'))
    death_age = db.Column(db.Integer, nullable=True)
    cause = db.Column(db.String(256), nullable=False)


class Father(db.Model):
    __tablename__ = "father"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'))
    death_age = db.Column(db.Integer, nullable=True)
    cause = db.Column(db.String(256), nullable=False)


class Sister(db.Model):
    __tablename__ = "sister"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'))
    death_age = db.Column(db.Integer, nullable=True)
    cause = db.Column(db.String(256), nullable=False)


class Brother(db.Model):
    __tablename__ = "brother"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'))
    death_age = db.Column(db.Integer, nullable=True)
    cause = db.Column(db.String(256), nullable=False)


class FamilyHistory(db.Model):
    __tablename__ = "family_history"
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'), primary_key=True)
    heart_disease = db.Column(db.String(256), nullable=False)
    diabetes = db.Column(db.String(256), nullable=False)
    high_blood_pressure = db.Column(db.String(256), nullable=False)
    stroke = db.Column(db.String(256), nullable=False)
    varicose_veins = db.Column(db.String(256), nullable=False)
    gout = db.Column(db.String(256), nullable=False)
    arthritis = db.Column(db.String(256), nullable=False)
    neuropathy = db.Column(db.String(256), nullable=False)
    bleeding_disorder = db.Column(db.String(256), nullable=False)
    foot_problems = db.Column(db.String(256), nullable=False)
    brothers = db.relationship('Brother', backref='patient')
    sisters = db.relationship('Sister', backref='patient')
    mother = db.relationship('Mother', backref='patient')
    father = db.relationship('Father', backref='patient')


class InviteCode(db.Model):
    __tablename__ = "invite_code"
    invite_code = db.Column(db.Integer, index=True, primary_key=True)
