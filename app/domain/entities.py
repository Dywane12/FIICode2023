from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login_manager


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
    medical_record_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), index=True, unique=False, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    consultation = db.relationship('Consultation', backref='patient', lazy='dynamic')

    # profile = db.image_attachment("PatientPicture")

    def __init__(self, username, first_name, last_name, phone_number, email, address, id_series, id_number, cnp,
                 birth_date, marital_status, gender, medical_record_id, doctor_id, password_hash):
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
        self.medical_record_id = medical_record_id
        self.password_hash = password_hash
        self.doctor_id = doctor_id

    def set_username(self, value):
        self.username = value

    def set_first_name(self, value):
        self.first_name = value

    def set_last_name(self, value):
        self.last_name = value

    def set_phone_number(self, value):
        self.phone_number = value

    def set_email(self, value):
        self.email = value

    def set_address(self, value):
        self.address = value

    def set_id_series(self, value):
        self.id_series = value

    def set_id_number(self, value):
        self.id_number = value

    def set_cnp(self, value):
        self.cnp = value

    def set_birth_date(self, value):
        self.birth_date = value

    def set_marital_status(self, value):
        self.marital_status = value

    def set_gender(self, value):
        self.gender = value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    def __init__(self, username, first_name, last_name, phone_number, email, address, birth_date,
                 gender, consultation_schedule_office, consultation_schedule_away, assistants_schedule, password_hash):
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

    def set_username(self, value):
        self.username = value

    def set_first_name(self, value):
        self.first_name = value

    def set_last_name(self, value):
        self.last_name = value

    def set_phone_number(self, value):
        self.phone_number = value

    def set_email(self, value):
        self.email = value

    def set_address(self, value):
        self.address = value

    def set_birth_date(self, value):
        self.birth_date = value

    def set_gender(self, value):
        self.gender = value

    def set_consultation_schedule_office(self, value):
        self.consultation_schedule_office = value

    def set_consultation_schedule_away(self, value):
        self.consultation_schedule_away = value

    def set_assistants_schedule(self, value):
        self.assistants_schedule = value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
