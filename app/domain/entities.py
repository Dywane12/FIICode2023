from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login_manager
from hashlib import md5


class Patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    phone_number = db.Column(db.Integer, index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    address = db.Column(db.String(256), index=True, nullable=False)
    id_series = db.Column(db.String(8), index=True, nullable=False)
    id_number = db.Column(db.String(16), index=True, unique=True, nullable=False)
    cnp = db.Column(db.Integer, index=True, nullable=False)
    birth_date = db.Column(db.String(128), index=True, nullable=False)
    marital_status = db.Column(db.String(16), index=True, nullable=False)
    gender = db.Column(db.String(8), index=True, nullable=False)
    occupation = db.Column(db.String(256), nullable=True)
    medical_record_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), index=True, unique=False, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    consultation = db.relationship('Consultation', backref='patient', lazy='dynamic')

    # profile = db.image_attachment("PatientPicture")

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None, id_series=None, id_number=None, cnp=None,
                 birth_date=None, marital_status=None, gender=None, occupation=None, medical_record_id=None, doctor_id=None, password_hash=None):
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
    patients = db.relationship('Patient', backref='doctor', lazy='dynamic')
    consultations = db.relationship('Consultation', backref='doctor', lazy='dynamic')

    def __init__(self, username=None, first_name=None, last_name=None, phone_number=None, email=None, address=None, birth_date=None,
                 gender=None, consultation_schedule_office=None, consultation_schedule_away=None, assistants_schedule=None, password_hash=None):
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
    id = db.Column(db.Integer, index=True, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    time = db.Column(db.String(128), index=True, nullable=False)
    pdf = db.Column(db.String(128), nullable=True)

    def __init__(self, patient_id, doctor_id, time, pdf):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.time = time
        self.pdf = pdf


class InviteCode(db.Model):
    invite_code = db.Column(db.Integer, index=True, primary_key=True)
