import random
import smtplib
from datetime import date, timedelta, datetime
import names
import random_address
from PyPDF2 import PdfFileMerger
from RandomDataGenerators import *
from random import randint
from geopy.geocoders import Nominatim
from geopy import distance
import re
from pdfminer.high_level import extract_text
from app import app
from app.domain.entities import Patient, Doctor, Consultation, Drinker, Smoker, InformationSheet, Father, FamilyHistory, \
    Mother, Brother, Sister, Hospitalization, ChronicDisease, Allergy, InviteCode
from twilio.rest import Client
import os
from werkzeug.utils import secure_filename
import phone_gen
FOLDER = os.path.abspath(os.path.join(app.root_path,'static/files'))
ALLOWED_EXTENSIONS = {'jpg', 'pdf'}
USERNAME_DOCTOR = 0
FIRST_NAME_DOCTOR = 1
LAST_NAME_DOCTOR = 2
EMAIL_DOCTOR = 3
PHONE_NUMBER_DOCTOR = 4
ADDRESS_DOCTOR = 5
BIRTH_DATE_DOCTOR = 6
CONSULTATION_SCHEDULE_OFFICE_DOCTOR = 7
CONSULTATION_SCHEDULE_AWAY_DOCTOR = 8
ASSISTANTS_SCHEDULE_DOCTOR = 9
PASSWORD_DOCTOR = 10
GENDER_DOCTOR = 11
MEDICAL_PROOF = 12
ZIPCODE_DOCTOR = 13
CITY_DOCTOR = 14
COUNTY_DOCTOR = 15
PROFILE_PICTURE_DOCTOR = 16


USERNAME_PATIENT = 0
FIRST_NAME_PATIENT = 1
LAST_NAME_PATIENT = 2
EMAIL_PATIENT = 3
PHONE_NUMBER_PATIENT = 4
ADDRESS_PATIENT = 5
ZIP_CODE_PATIENT = 6
CITY_PATIENT = 7
COUNTY_PATIENT = 8
PASSPORT_ID_PATIENT = 9
BIRTH_DATE_PATIENT = 10
MARITAL_STATUS_PATIENT = 11
GENDER_PATIENT = 12
OCCUPATION_PATIENT = 13
PASSWORD_PATIENT = 14
INVITE_CODE_PATIENT = 15
PROFILE_PICTURE_PATIENT = 16


class Service:
    def __init__(self, db, session, choice=False):
        self.session = session
        self.db = db
        if choice:
            # self.__add_chronic_diseases()
            # self.__add_allergies()
            self.__add_fake_doctors(5)
            self.__add_fake_patients(10)
            self.__add_fake_consultations(15)

    def __add_chronic_diseases(self):
        chronic_diseases = [
            {'name': 'AIDS/HIV'}, {'name': 'Anemia'}, {'name': 'Anxiety'}, {'name': 'Arthritis'},
            {'name': 'Artificial Heart Valve'}, {'name': 'Artificial Joint'},
            {'name': 'Asthma'}, {'name': 'Back Problems'}, {'name': 'Bleeding Disorder'}, {'name': 'Bipolar Disorder'},
            {'name': 'Bloot Clot/DVT'},
            {'name': 'Bypass Surgery'},
            {'name': 'Cancer'}, {'name': 'Chemical Dependency'}, {'name': 'Chest Pain'},
            {'name': 'Circulatory Problems'}, {'name': 'Depression'},
            {'name': 'Diabetes' 'How long'}, {'name': 'Emphysema'},
            {'name': 'Eye Problems'}, {'name': 'Fibromyalgia'}, {'name': 'Fott Cramps'}, {'name': 'Gastric Reflux'},
            {'name': 'Gout'}, {'name': 'Headaches'},
            {'name': 'Heart Attack'}, {'name': 'Heart Murmur'},
            {'name': 'Heart Failure'}, {'name': 'Hemophilia'}, {'name': 'Hepatitis'}, {'name': 'High Blood Pressure'},
            {'name': 'Kidney Problems'},
            {'name': 'Leg Cramps'},
            {'name': 'Liver Disease'}, {'name': 'Low Blood Pressure'}, {'name': 'Mental Illness'},
            {'name': 'Neuropathy'}, {'name': 'Pacemaker'},
            {'name': 'Paralysis'}, {'name': 'Phlebitis'},
            {'name': 'Psoriasis'}, {'name': 'Rheumatic Fever'}, {'name': 'Schizophrenia'},
            {'name': 'Shortness of Breath'}, {'name': 'Stroke'},
            {'name': 'Thyroid Problems'},
            {'name': 'Tuberculosis'}, {'name': 'Ulcers (Stomach)'}, {'name': 'Varicose Veins'},
            {'name': 'Wight loss, unexplained'},
            {'name': 'Pregnant?'}, {'name': 'Breastfeeding?'}
        ]
        for disease in chronic_diseases:
            given_chronic_disease = ChronicDisease(name=disease['name'])
            self.db.add_entity(given_chronic_disease)
        self.db.save_to_database()

    def __add_allergies(self):
        allergies = [
            {'name': 'Local anesthesia'}, {'name': 'Aspirin'}, {'name': 'Anti-Inflammatory'}, {'name': 'Penicillin'},
            {'name': 'Sulfa'}, {'name': 'IVP dye'}, {'name': 'Tetanus'}, {'name': 'General anesthesia'},
            {'name': 'Latex'}, {'name': 'Tape/Adhesives'}, {'name': 'Iodine'}, {'name': 'Betadine'},
            {'name': 'Codeine'}, {'name': 'Steroids'}
        ]
        for allergy in allergies:
            given_allergy = Allergy(name=allergy['name'])
            self.db.add_entity(given_allergy)
        self.db.save_to_database()

    def __add_fake_patients(self, n):
        zip_codes = [90011, 91331, 90650, 90201, 90250, 90044, 90805, 90280, 91342, 91744,
                     91335, 91706, 90706, 90003, 93550, 90255, 93535, 91766, 90262, 91402,
                     93536, 90631, 90026, 90022, 91343, 90037, 90660, 90019, 91770, 90640,
                     90042, 90001, 90066, 91732, 90004, 90006, 90731, 91702, 90813, 91406,
                     90744, 91605, 91405, 91304, 91801, 91745, 90723, 93551, 90018, 90063,
                     90745, 90221, 90002, 90034, 91344, 90047, 90220, 90046, 91767, 90703,
                     90023, 90065, 90638, 90057, 90032, 91306, 90033, 91789, 90025, 91352,
                     91790, 90027, 91733, 90247, 90016, 90007, 90059, 90043, 90024, 91765,
                     91367, 90503, 90241, 91748, 90242, 92821, 90604, 90806, 91311, 91355,
                     91606, 91016, 90045]
        for i in range(n):
            doctor = random.choice(self.get_all_doctors())
            patient = Patient(doctor_id=doctor.id)
            gender = random.choice(['Male', 'Female'])
            first_name, last_name = names.get_full_name(gender=gender.lower()).split()
            username = first_name + '_' + last_name + f'{randint(1, 420)}'
            phone_number = phone_gen.PhoneNumber("US").get_number()
            email = first_name + '_' + last_name + f'{randint(1, 420)}' + '@gmail.com'
            address_data = random_address.real_random_address_by_state('CA')
            address = address_data['address1']
            city = address_data['city']
            state = 'CA'
            postal_code = address_data['postalCode']
            passport_id = randint(1000000, 9999999)
            occupation = random_pretentious_job_title(1, number_of_words=2)
            birth_date = self.__random_date(date(1940, 1, 1), date(2008, 12, 30))
            marital_status = random.choice(['Married', 'Divorced', 'Widow', 'Single'])
            patient.gender = gender
            patient.email = email
            patient.address = address
            patient.birth_date = birth_date
            patient.last_name = last_name
            patient.first_name = first_name
            patient.username = username
            patient.state = state
            patient.city = city
            patient.postalcode = postal_code
            patient.passport_id = passport_id
            patient.occupation = occupation
            patient.marital_status = marital_status
            patient.phone_number = phone_number
            self.db.add_entity(patient)
            self.db.save_to_database()
            information_sheet = InformationSheet(patient_id=patient.id)
            if gender == 'Female':
                height = randint(140, 185)
            else:
                height = randint(160, 210)
            weight = height // 2.8
            shoe_size = height // 4.05
            blood_type = random.choice(['0', 'A', 'AB', "B"])
            information_sheet.height = height
            information_sheet.weight = weight
            information_sheet.shoe_size = shoe_size
            information_sheet.blood_type = blood_type
            choice = random.choice([True, False])
            if choice:
                for chronic_disease in self.db.find_all_chronic_diseases():
                    if len(information_sheet.medical_history) > 3:
                        break
                    choice = random.choice([True, False])
                    if choice:
                        information_sheet.medical_history.append(chronic_disease)
            choice = random.choice([True, False])
            if choice:
                for allergy in self.db.find_all_allergies():
                    if len(information_sheet.allergies) > 3:
                        break
                    choice = random.choice([True, False])
                    if choice:
                        information_sheet.allergies.append(allergy)
            number_of_hospitalizations = randint(0, 5)
            for _ in range(number_of_hospitalizations):
                hospitalization = Hospitalization()
                hospitalization.patient_id = patient.id
                hospitalization_date = self.__random_date(date(2010, 1, 1), datetime.now().date())
                hospitalization.date = hospitalization_date
                self.db.add_entity(hospitalization)
            is_smoking = randint(0, 1)
            if is_smoking:
                current_packs_per_day = randint(1, 5)
                smoking_years = randint(0, 10)
                smoker = Smoker(current_packs_per_day=current_packs_per_day, smoking_years=smoking_years)
                smoker.patient_id = patient.id
                self.db.add_entity(smoker)
            else:
                was_smoking = randint(0, 1)
                if was_smoking:
                    previous_pack_per_day = randint(1, 5)
                    smoking_years = randint(0, 10)
                    smoker = Smoker(previous_pack_per_day=previous_pack_per_day, smoking_years=smoking_years)
                    smoker.patient_id = patient.id
                    self.db.add_entity(smoker)
            is_drinking = randint(0, 1)
            if is_drinking:
                quantity = randint(1, 5)
                frequency = randint(1, 7)
                drinker = Drinker(quantity, frequency)
                drinker.patient_id = patient.id
                self.db.add_entity(drinker)
            password = 'nacho'
            patient.set_password(password)
            self.db.add_entity(information_sheet)
            invite_code = InviteCode(invite_code=self.generate_random_code(), patient_id=patient.id,
                                     doctor_id=patient.doctor_id)
            self.db.add_entity(invite_code)
            self.db.save_to_database()

    def __add_fake_doctors(self, n):
        zip_codes = [90011, 91331, 90650, 90201, 90250, 90044, 90805, 90280, 91342, 91744,
                     91335, 91706, 90706, 90003, 93550, 90255, 93535, 91766, 90262, 91402,
                     93536, 90631, 90026, 90022, 91343, 90037, 90660, 90019, 91770, 90640,
                     90042, 90001, 90066, 91732, 90004, 90006, 90731, 91702, 90813, 91406,
                     90744, 91605, 91405, 91304, 91801, 91745, 90723, 93551, 90018, 90063,
                     90745, 90221, 90002, 90034, 91344, 90047, 90220, 90046, 91767, 90703,
                     90023, 90065, 90638, 90057, 90032, 91306, 90033, 91789, 90025, 91352,
                     91790, 90027, 91733, 90247, 90016, 90007, 90059, 90043, 90024, 91765,
                     91367, 90503, 90241, 91748, 90242, 92821, 90604, 90806, 91311, 91355,
                     91606, 91016, 90045]
        for i in range(n):
            gender = random.choice(['Male', 'Female'])
            first_name, last_name = names.get_full_name(gender=gender.lower()).split()
            username = first_name + '_' + last_name + f'{randint(1, 420)}'
            phone_number = phone_gen.PhoneNumber("US").get_number()
            email = first_name + '_' + last_name + f'{randint(1, 420)}' + '@gmail.com'
            address_data = random_address.real_random_address_by_state('CA')
            address = address_data['address1']
            city = address_data['city']
            state = 'CA'
            postal_code = address_data['postalCode']
            birth_date = self.__random_date(date(1960, 1, 1), date(1995, 12, 30))
            consultation_schedule_office = self.__random_schedule()
            consultation_schedule_away = consultation_schedule_office
            while consultation_schedule_office == consultation_schedule_away:
                consultation_schedule_away = self.__random_schedule()
            password = 'nacho'
            assistants_schedule = self.__random_schedule()
            doctor = Doctor(username=username, first_name=first_name, last_name=last_name, phone_number=phone_number,
                            email=email, address=address, city=city, state=state, postalcode=postal_code,
                            birth_date=birth_date, gender=gender, consultation_schedule_office
                            =''.join(day for day in consultation_schedule_office),
                            consultation_schedule_away=', '.join(day for day in consultation_schedule_away),
                            assistants_schedule=' , '.join(day for day in assistants_schedule))
            doctor.set_password(password)
            """medical_degree_date = {'university_name': "University of Nacho's",
                                   'student_name': f'{doctor.first_name} {doctor.last_name}',
                                   'date': (birth_date+timedelta(weeks=1565)),
                                   'graduation_year': (birth_date+timedelta(weeks=1565)).year}
            template_loader = jinja2.FileSystemLoader(‘./ ’)
            template_env = jinja2.Environment(loader=template_loader)"""
            self.db.add_entity(doctor)
        self.db.save_to_database()

    def __add_fake_consultations(self, n):
        for i in range(n):
            patient = random.choice(self.get_all_patients())
            doctor_id = patient.doctor_id
            time = self.__random_date(date(2015, 1, 1), datetime.now().date())
            pdf = randint(100, 1000 - 1)
            urgency_grade = randint(1, 5)
            consultation = Consultation(patient_id=patient.id, doctor_id=doctor_id, time=time, pdf=pdf,
                                        urgency_grade=urgency_grade)
            self.db.add_entity(consultation)
        self.db.save_to_database()

    @staticmethod
    def __random_date(start_date, end_date):
        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        return start_date + timedelta(days=rand_days)

    @staticmethod
    def __random_working_hours():
        start_hour = randint(8, 14)
        end_hour = randint(start_hour + 2, 18)
        return f'{start_hour}:00-{end_hour}:00'

    @staticmethod
    def __random_working_days():
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        number_of_working_days = randint(2, 5)
        working_days = random.sample(weekdays, number_of_working_days)
        return working_days

    def __random_schedule(self):
        schedule = []
        for day in self.__random_working_days():
            schedule.append(f'{day}: {self.__random_working_hours()}')
        return schedule

    def register_medic(self, register_data):
        doctor = Doctor()
        medical_proof = register_data[MEDICAL_PROOF]
        doctor.username = register_data[USERNAME_DOCTOR]
        if medical_proof.filename == '':
            raise ValueError("No medical proof found")
        if not self.allowed_file(medical_proof.filename):
            raise ValueError("Invalid file format")
        medical_proof.filename = f'{doctor.username}.pdf'
        medical_proof_path = self.save_file(medical_proof, 'proofs')
        if not self.validate_medical_proof(os.path.abspath(medical_proof_path),
                                           register_data[FIRST_NAME_DOCTOR] + ' ' + register_data[LAST_NAME_DOCTOR]):
            os.remove(os.path.abspath(medical_proof_path))
            raise AttributeError("Invalid proof")
        doctor.medical_proof = medical_proof.filename
        if (register_data[USERNAME_DOCTOR] == "" or register_data[PASSWORD_DOCTOR] == "" or register_data[FIRST_NAME_DOCTOR] == "" or
                register_data[LAST_NAME_DOCTOR] == "" or
                register_data[EMAIL_DOCTOR] == "" or register_data[PHONE_NUMBER_DOCTOR] == "" or register_data[
                    ADDRESS_DOCTOR] == "" or
                register_data[BIRTH_DATE_DOCTOR] == "" or
                register_data[CONSULTATION_SCHEDULE_OFFICE_DOCTOR] == "" or register_data[
                    CONSULTATION_SCHEDULE_AWAY_DOCTOR] == "" or
                register_data[ASSISTANTS_SCHEDULE_DOCTOR] == "" or register_data[GENDER_DOCTOR] == "" or register_data[ZIPCODE_DOCTOR] == ''
                or register_data[CITY_DOCTOR]=='' or register_data[COUNTY_DOCTOR]=='' or register_data[PROFILE_PICTURE_DOCTOR]==''):
            raise ValueError("Invalid data")
        doctors = self.get_all_doctors()
        for doctor_in_database in doctors:
            if doctor.username == doctor_in_database.username:
                raise ValueError("Username already exists")
        profile_picture = register_data[PROFILE_PICTURE_DOCTOR]
        profile_picture.filename = f'{doctor.username}.jpg'
        self.save_file(profile_picture, 'profile_picture_doctor')
        doctor.profile_picture = profile_picture.filename
        doctor.first_name = register_data[FIRST_NAME_DOCTOR]
        doctor.last_name = register_data[LAST_NAME_DOCTOR]
        doctor.email = register_data[EMAIL_DOCTOR]
        for doctor_in_database in doctors:
            if doctor.email == doctor_in_database.email:
                raise ValueError("Email already registered")
        doctor.phone_number = register_data[PHONE_NUMBER_DOCTOR]
        for doctor_in_database in doctors:
            if doctor.phone_number == doctor_in_database.phone_number:
                raise ValueError("Phone number already registered")
        doctor.address = register_data[ADDRESS_DOCTOR]
        doctor.zipcode = register_data[ZIPCODE_DOCTOR]
        doctor.city = register_data[CITY_DOCTOR]
        doctor.state = register_data[COUNTY_DOCTOR]
        doctor.birth_date = register_data[BIRTH_DATE_DOCTOR]
        doctor.consultation_schedule_office = register_data[CONSULTATION_SCHEDULE_OFFICE_DOCTOR]
        doctor.consultation_schedule_away = register_data[CONSULTATION_SCHEDULE_AWAY_DOCTOR]
        doctor.assistants_schedule = register_data[ASSISTANTS_SCHEDULE_DOCTOR]
        doctor.set_password(register_data[PASSWORD_DOCTOR])
        doctor.gender = register_data[GENDER_DOCTOR]
        self.db.add_entity(doctor)

    def register_patient(self, register_data):
        patient = Patient()
        self.db.add_entity(patient)
        for invite_code in self.db.find_all_invite_codes():
            if int(register_data[INVITE_CODE_PATIENT]) == invite_code.invite_code and invite_code.patient_id is not None:
                raise ValueError("Invalid invite code")
        invite_code = self.db.find_invite_code(int(register_data[INVITE_CODE_PATIENT]))
        if invite_code.patient_id is not None:
            raise ValueError("Invite code already used")
        if (register_data[USERNAME_PATIENT] == "" or register_data[FIRST_NAME_PATIENT] == "" or register_data[
            LAST_NAME_PATIENT] == "" or
                register_data[EMAIL_PATIENT] == ""
                or register_data[PHONE_NUMBER_PATIENT] == "" or register_data[ADDRESS_PATIENT] == ""
                or register_data[MARITAL_STATUS_PATIENT] == "" or register_data[
                    PASSWORD_PATIENT] == "" or register_data[GENDER_PATIENT] == "" or register_data[
                    ZIP_CODE_PATIENT] == ""
                or register_data[CITY_PATIENT] == "" or register_data[COUNTY_PATIENT] == "" or register_data[
                    PASSPORT_ID_PATIENT] == ""
                or register_data[BIRTH_DATE_PATIENT] == "" or register_data[OCCUPATION_PATIENT] == "" or register_data[
                    INVITE_CODE_PATIENT] == "" or register_data[PROFILE_PICTURE_PATIENT]==''):
            raise ValueError("Empty fields")
        patient.username = register_data[USERNAME_PATIENT]
        patients = self.get_all_patients()
        for patient_in_database in patients:
            if patient.username == patient_in_database.username:
                raise ValueError("Username already exists")
        profile_picture = register_data[PROFILE_PICTURE_PATIENT]
        profile_picture.filename = f'{patient.username}.jpg'
        self.save_file(profile_picture, 'profile_picture_patient')
        patient.profile_picture = profile_picture.filename
        patient.first_name = register_data[FIRST_NAME_PATIENT]
        patient.last_name = register_data[LAST_NAME_PATIENT]
        patient.email = register_data[EMAIL_PATIENT]
        for patient_in_database in patients:
            if patient.email == patient_in_database.email:
                raise ValueError("Email already registered")
        patient.phone_number = register_data[PHONE_NUMBER_PATIENT]
        for patient_in_database in patients:
            if patient.phone_number == patient_in_database.phone_number:
                raise ValueError("Phone number already registered")
        patient.address = register_data[ADDRESS_PATIENT]
        patient.postalcode = register_data[ZIP_CODE_PATIENT]
        patient.city = register_data[CITY_PATIENT]
        patient.state = register_data[COUNTY_PATIENT]
        patient.passport_id = register_data[PASSPORT_ID_PATIENT]
        for patient_in_database in patients:
            if patient.passport_id == patient_in_database.passport_id:
                raise ValueError("Passport id already registered")
        patient.birth_date = register_data[BIRTH_DATE_PATIENT]
        patient.occupation = register_data[OCCUPATION_PATIENT]
        patient.martial_status = register_data[MARITAL_STATUS_PATIENT]
        patient.set_password(register_data[PASSWORD_PATIENT])
        patient.gender = register_data[GENDER_PATIENT]
        patient.doctor_id = invite_code.doctor_id
        invite_code.patient_id = patient.id
        return patient.id

    def get_all_doctors(self):
        return self.db.find_all_doctors()

    def get_all_patients(self):
        return self.db.find_all_patients()

    def get_doctor_patients(self):
        return self.get_doctor_by_id(self.session['doctor']).patients

    def get_doctor_by_username(self, username):
        """
        Calls the find_doctor_username function from the repository
        :param username: str
        :return: True/False
        """
        return self.db.find_doctor_username(username)

    def get_patient_by_username(self, username):
        """
        Calls the find_patient_username function from the repository
        :param username: str
        :return: True/False
        """
        return self.db.find_patient_username(username)

    def get_doctor_by_id(self, doctor_id):
        return self.db.find_doctor_by_id(doctor_id)

    def get_patient_by_id(self, patient_id):
        return self.db.find_patient_by_id(patient_id)

    def update_database(self):
        self.db.save_to_database()

    @staticmethod
    def update_doctor_profile(doctor, update_data):
        if update_data[USERNAME_DOCTOR] != "":
            doctor.username = update_data[USERNAME_DOCTOR]
        if update_data[FIRST_NAME_DOCTOR] != "":
            doctor.first_name = update_data[FIRST_NAME_DOCTOR]
        if update_data[LAST_NAME_DOCTOR] != "":
            doctor.last_name = update_data[LAST_NAME_DOCTOR]
        if update_data[EMAIL_DOCTOR] != "":
            doctor.email = update_data[EMAIL_DOCTOR]
        if update_data[PHONE_NUMBER_DOCTOR] != "":
            doctor.phone_number = update_data[PHONE_NUMBER_DOCTOR]
        if update_data[ADDRESS_DOCTOR] != "":
            doctor.address = update_data[ADDRESS_DOCTOR]
        if update_data[BIRTH_DATE_DOCTOR] != "":
            doctor.birth_date = update_data[BIRTH_DATE_DOCTOR]
        if update_data[CONSULTATION_SCHEDULE_OFFICE_DOCTOR] != "":
            doctor.consultation_schedule_office = update_data[CONSULTATION_SCHEDULE_OFFICE_DOCTOR]
        if update_data[CONSULTATION_SCHEDULE_AWAY_DOCTOR] != "":
            doctor.consultation_schedule_away = update_data[CONSULTATION_SCHEDULE_AWAY_DOCTOR]
        if update_data[ASSISTANTS_SCHEDULE_DOCTOR] != "":
            doctor.assistants_schedule = update_data[ASSISTANTS_SCHEDULE_DOCTOR]
        if update_data[PASSWORD_DOCTOR] != "":
            doctor.set_password(update_data[PASSWORD_DOCTOR])

    @staticmethod
    def update_patient_profile(patient, update_data):
        if update_data[USERNAME_PATIENT] != "":
            patient.username = update_data[USERNAME_PATIENT]
        if update_data[FIRST_NAME_PATIENT] != "":
            patient.first_name = update_data[FIRST_NAME_PATIENT]
        if update_data[LAST_NAME_PATIENT] != "":
            patient.last_name = update_data[LAST_NAME_PATIENT]
        if update_data[EMAIL_PATIENT] != "":
            patient.email = update_data[EMAIL_PATIENT]
        if update_data[PHONE_NUMBER_PATIENT] != "":
            patient.phone_number = update_data[PHONE_NUMBER_PATIENT]
        if update_data[ADDRESS_PATIENT] != "":
            patient.address = update_data[ADDRESS_PATIENT]
        if update_data[ZIP_CODE_PATIENT] != "":
            patient.postalcode = update_data[ZIP_CODE_PATIENT]
        if update_data[PASSPORT_ID_PATIENT] != "":
            patient.passport_id = update_data[PASSPORT_ID_PATIENT]
        if update_data[BIRTH_DATE_PATIENT] != "":
            patient.birth_date = update_data[BIRTH_DATE_PATIENT]
        if update_data[OCCUPATION_PATIENT] != "":
            patient.occupation = update_data[OCCUPATION_PATIENT]
        if update_data[CITY_PATIENT] != "":
            patient.city = update_data[CITY_PATIENT]
        if update_data[COUNTY_PATIENT] != "":
            patient.state = update_data[COUNTY_PATIENT]
        if update_data[INVITE_CODE_PATIENT] != "":
            patient.invite_code = update_data[INVITE_CODE_PATIENT]
        if update_data[MARITAL_STATUS_PATIENT] != "":
            patient.martial_status = update_data[MARITAL_STATUS_PATIENT]
        if update_data[PASSWORD_PATIENT] != "":
            patient.set_password(update_data[PASSWORD_PATIENT])
        if update_data[GENDER_PATIENT] != "":
            patient.gender = update_data[GENDER_PATIENT]

    @staticmethod
    def generate_random_code():
        #fagssdfg
        return random.randint(1000000, 9999999)


    def send_welcome_email(self, email_patient, email_companie):
        sender_account = email_companie
        reciever_account = email_patient
        cod = self.generate_random_code()
        invite_code = InviteCode(invite_code=cod, doctor_id=self.session['doctor'])
        self.db.add_entity(invite_code)
        self.update_database()
        message = f"Subject: WELCOME TO OUR CLINIC!!\nYour code is:{cod}"
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_account, "your_password")
            server.sendmail(sender_account, reciever_account, message)

    def send_welcome_sms(self, destination_number):
        sender_number = "+40772093773"
        account_sid = "ACe49ff3d982fa8beb419253807c8314a2"
        auth_token = "dee13ecedc920689c09a553114f75879"
        client = Client(account_sid, auth_token)
        cod = self.generate_random_code()
        invite_code = InviteCode(invite_code=cod, doctor_id=self.session['doctor'])
        self.db.add_entity(invite_code)
        self.update_database()
        message_body = f"Subject: WELCOME TO OUR CLINIC!!\nYour code is:{cod}"
        destination_number = "+40" + destination_number
        client.messages.create(
            to=destination_number,
            from_=sender_number,
            body=message_body)

    def create_appointment_ad_hoc(self, time, urgency_grade):
        doctor_id = self.session['doctor']
        consultation = Consultation(doctor_id=doctor_id, time=time, urgency_grade=urgency_grade)
        self.db.add_entity(consultation)
        self.db.save_to_database()

    def create_appointment_registered_patient(self, time, urgency_grade):
        patient = self.get_patient_by_id(self.session['patient'])
        consultation = Consultation(doctor_id=patient.doctor_id, patient_id=patient.id, time=time,
                                    urgency_grade=urgency_grade)
        self.db.add_entity(consultation)
        self.update_database()

    def get_doctors_nearby_patient(self, patient_id):
        geolocator = Nominatim(user_agent="medical_app")
        patient = self.get_patient_by_id(patient_id)
        patient_location = geolocator.geocode(patient.address + ' ' + patient.state)
        doctors_nearby = []
        for doctor in self.get_all_doctors():
            doctor_location = geolocator.geocode(doctor.address + ' ' + doctor.state)
            distance_doctor_to_patient = distance.distance((patient_location.latitude, patient_location.longitude),
                                                           (doctor_location.latitude, doctor_location.longitude)).km
            if distance_doctor_to_patient < 30:
                doctors_nearby.append(doctor)
        return doctors_nearby

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_file(self, file, folder):
        filename = secure_filename(file.filename)
        file_path = os.path.abspath(os.path.join(os.path.abspath(os.path.join(app.root_path,'static/files')), folder, filename))
        file.save(file_path)
        return file_path

    @staticmethod
    def validate_medical_proof(file_path, medic_name):
        text = extract_text(file_path)
        is_medic = re.compile('{}'.format(medic_name), re.IGNORECASE)
        medic_name_matches = is_medic.findall(text)
        if len(medic_name_matches) == 0:
            return False
        is_medical_degree = re.compile("Medical Degree", re.IGNORECASE)
        medical_degree_matches = is_medical_degree.findall(text)
        if len(medical_degree_matches) == 0:
            return False
        is_university = re.compile("University", re.IGNORECASE)
        university_matches = is_university.findall(text)
        if len(university_matches) == 0:
            return False
        return True

    def add_consultation(self, patient_id, time, urgency_grade, pdf=None):
        consultation = Consultation(doctor_id=self.session['doctor'], patient_id=patient_id, time=time,
                                    urgency_grade=urgency_grade)
        if pdf is not None:
            pdf_path = self.save_file(pdf, 'consultation')
            consultation.pdf = pdf_path
        self.db.add_entity(consultation)
        self.db.save_to_database()

    def add_pdf_to_consultation(self, consultation_id, pdf):
        consultation = self.db.find_consultation_by_id(consultation_id)
        if consultation is None:
            raise ValueError("Invalid id")
        if consultation.pdf is not None:
            pdf.filename = f'{consultation_id}_extension.pdf'
            self.save_file(pdf, 'consultation')
            merger = PdfFileMerger()
            pdfs_merge = [os.path.abspath(os.path.join(FOLDER, consultation.pdf)),
                          os.path.abspath(os.path.join(FOLDER, pdf.filename))]
            for pdf_merge in pdfs_merge:
                merger.append(pdf_merge)
            merger.write(os.path.abspath(os.path.join(FOLDER, consultation.pdf)))
            merger.close()
            os.remove(os.path.abspath(os.path.join(FOLDER, pdf.filename)))
        else:
            pdf.filename = f'{consultation_id}.pdf'
            self.save_file(pdf, 'consultation')

    def transfer_patient(self, patient_id, doctor_id):
        patient = self.get_patient_by_id(patient_id)
        patient.doctor_id = doctor_id

    def get_patients_that_want_to_transfer(self):
        patients_that_want_to_transfer = []
        for patient in self.get_doctor_patients():
            if patient.transfer == 1:
                patients_that_want_to_transfer.append(patient)
        return patients_that_want_to_transfer

    def get_consultation(self, consultation_id):
        return self.db.find_consultation_by_id(consultation_id)

    def update_consultation_time(self, consultation_id, time):
        consultation = self.db.find_consultation_by_id(consultation_id)
        consultation.date_time = time
        self.update_database()

    def update_consultation_urgency_grade(self, consultation_id, urgency_grade):
        consultation = self.db.find_consultation_by_id(consultation_id)
        consultation.urgency_grade = urgency_grade
        self.update_database()

    def get_consultation_history(self, patient_id):
        patient = self.db.find_patient_by_id(patient_id)
        if patient is None:
            raise ValueError("Patient not found")
        consultation_history = []
        for consultation in patient.consultations:
            if consultation.date_time < datetime.now():
                consultation_history.append(consultation)
        return consultation_history

    def get_future_consultations(self, patient_id):
        patient = self.db.find_patient_by_id(patient_id)
        if patient is None:
            raise ValueError("Patient not found")
        future_consulations = []
        for consultation in patient.consultations:
            if consultation.date_time > datetime.now():
                future_consulations.append(consultation)
        return future_consulations

    def register_information_sheet_1(self, form_data, patient_id, diseases):
        information_sheet = InformationSheet(patient_id=patient_id)
        for disease in diseases:
            if form_data[disease['name']] == "":
                raise ValueError("Empty fields")
        for disease in diseases:
            information_sheet.medical_history.append(self.db.find_disease_by_name(form_data[disease['name']]))
        self.db.add_entity(information_sheet)
        return information_sheet.id

    def register_information_sheet_2(self, form_data, information_sheet_id, diseases):
        information_sheet = self.db.find_information_sheet_by_id(information_sheet_id)
        for disease in diseases:
            if form_data[disease['name']] == "":
                raise ValueError("Empty fields")
        for disease in diseases:
            information_sheet.medical_history.append(self.db.find_disease_by_name(form_data[disease['name']]))
        return information_sheet.id

    def register_information_sheet_3(self, form_data, information_sheet_id, allergies):
        information_sheet = self.db.find_information_sheet_by_id(information_sheet_id)
        for allergy in allergies:
            if form_data[allergy['name']] == "":
                raise ValueError("Empty fields")
        for allergy in allergies:
            information_sheet.allergies.append(self.db.find_allergy_by_name(form_data[allergy['name']]))
        return information_sheet.id

    def link_patient_to_information_sheet(self):
        information_sheet = self.db.find_information_sheet_by_id(self.session['information_sheet_id'])
        information_sheet.patient_id = self.session['patient_id']
