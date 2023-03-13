from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login_manager
from hashlib import md5


class Patient(UserMixin, db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    phone_number = db.Column(db.Integer, index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    address = db.Column(db.String(256), index=True, nullable=False)
    postalcode = db.Column(db.String(256), index=True, nullable=False)
    city = db.Column(db.String(256), index=True, nullable=False)
    county = db.Column(db.String(256), index=True, nullable=False)
    passport_id = db.Column(db.String(16), index=True, unique=True, nullable=False)
    cnp = db.Column(db.Integer, index=True, nullable=False)
    birth_date = db.Column(db.String(128), index=True, nullable=False)
    marital_status = db.Column(db.String(16), index=True, nullable=False)
    gender = db.Column(db.String(8), index=True, nullable=False)
    occupation = db.Column(db.String(256), nullable=True)
    password_hash = db.Column(db.String(256), index=True, unique=False, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    consultations = db.relationship('Consultation', backref='patient')
    information_sheet = db.relationship('InformationSheet', backref='patient')

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None,
                 id_series=None, id_number=None, cnp=None,
                 birth_date=None, marital_status=None, gender=None, occupation=None, medical_record_id=None,
                 doctor_id=None, password_hash=None):
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
    password_hash = db.Column(db.String(256), index=True, unique=False)
    patients = db.relationship('Patient', backref='doctor')
    consultations = db.relationship('Consultation', backref='doctor')

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None,
                 birth_date=None,
                 gender=None, consultation_schedule_office=None, consultation_schedule_away=None,
                 assistants_schedule=None, password_hash=None):
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
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    time = db.Column(db.DateTime, index=True, nullable=False)
    pdf = db.Column(db.String(128), nullable=True)
    urgency_grade = db.Column(db.String(128), nullable=True)

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
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), primary_key=True)
    weight = db.Column(db.Integer, index=True, nullable=False)
    height = db.Column(db.Integer, index=True, nullable=False)
    shoe_size = db.Column(db.Integer, index=True, nullable=False)
    blood_type = db.Column(db.String(256), index=True, nullable=False)
    medical_history = db.relationship('ChronicDisease', secondary=information_sheet_chronic_disease, backref='patients')
    medications = db.relationship('Drug', backref='patient')
    allergies = db.relationship('Allergy', secondary=information_sheet_allergy, backref='patients')
    hospitalization = db.relationship('Hospitalization', backref='patient')
    smoking = db.relationship('Smoker', backref='patient')
    drinking = db.relationship('Drinker', backref='patient')
    family_history = db.relationship('FamilyHistory', backref='patient')


class Mother(db.Model):
    __tablename__ = "mother"
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'), primary_key=True)
    living = db.Column(db.Integer, nullable=True)
    living_age = db.Column(db.Integer, nullable=True)
    death_age = db.Column(db.Integer, nullable=True)
    cause = db.Column(db.String(256), nullable=False)


class Father(db.Model):
    __tablename__ = "father"
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'), primary_key=True)
    living = db.Column(db.Integer, nullable=True)
    living_age = db.Column(db.Integer, nullable=True)
    death_age = db.Column(db.Integer, nullable=True)
    cause = db.Column(db.String(256), nullable=False)


class Sister(db.Model):
    __tablename__ = "sister"
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'), primary_key=True)
    living = db.Column(db.Integer, nullable=True)
    living_age = db.Column(db.Integer, nullable=True)
    death_age = db.Column(db.Integer, nullable=True)
    cause = db.Column(db.String(256), nullable=False)


class Brother(db.Model):
    __tablename__ = "brother"
    patient_id = db.Column(db.Integer, db.ForeignKey('family_history.patient_id'), primary_key=True)
    living = db.Column(db.Integer, nullable=True)
    living_age = db.Column(db.Integer, nullable=True)
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


class Smoker(db.Model):
    __tablename__ = "smoker"
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'), primary_key=True)
    is_smoking = db.Column(db.Integer, nullable=True)
    was_smoking = db.Column(db.Integer, nullable=True)
    current_packs_per_day = db.Column(db.Integer, nullable=True)
    previous_pack_per_day = db.Column(db.Integer, nullable=True)
    smoking_years = db.Column(db.Integer, nullable=True)


class Drinker(db.Model):
    __tablename__ = "drinker"
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'), primary_key=True)
    is_drinking = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    frequency = db.Column(db.Integer, nullable=True)


class Hospitalization(db.Model):
    __tablename__ = "hospitalization"
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'), primary_key=True)


class ChronicDisease(db.Model):
    __tablename__ = "chronic_disease"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, nullable=False)


class Drug(db.Model):
    __tablename__ = "drug"
    patient_id = db.Column(db.Integer, db.ForeignKey('information_sheet.patient_id'), primary_key=True)
    name = db.Column(db.String(256), index=True, nullable=False)
    dosage = db.Column(db.String(256), nullable=False)
    frequency = db.Column(db.String(256), nullable=False)


class Allergy(db.Model):
    __tablename__ = "allergy"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, nullable=False)


class InviteCode(db.Model):
    __tablename__ = "invite_code"
    invite_code = db.Column(db.Integer, index=True, primary_key=True)
