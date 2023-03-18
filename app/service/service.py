import random
import smtplib
from datetime import date, timedelta, datetime
import names
import random_address
from RandomDataGenerators import *
from random import randint
from geopy.geocoders import Nominatim
from geopy import distance
import re
from pdfminer.high_level import extract_text
import app
from app.domain.entities import Patient, Doctor, Consultation, Drinker, Smoker, InformationSheet, Father, FamilyHistory, \
    Mother, Brother, Sister, Hospitalization, ChronicDisease, Allergy
from twilio.rest import Client
import os
from werkzeug.utils import secure_filename
import phone_gen

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

USERNAME_PATIENT = 0
FIRST_NAME_PATIENT = 1
LAST_NAME_PATIENT = 2
EMAIL_PATIENT = 3
PHONE_NUMBER_PATIENT = 4
ADDRESS_PATIENT = 5
ZIP_CODE_PATIENT = 6#
CITY_PATIENT = 7#
COUNTY_PATIENT = 8#
PASSPORT_ID_PATIENT = 9#
BIRTH_DATE_PATIENT = 10#
MARITAL_STATUS_PATIENT = 11
GENDER_PATIENT = 12
OCCUPATION_PATIENT = 13#
PASSWORD_PATIENT = 14
INVITE_CODE_PATIENT = 15#


class Service:
    def __init__(self, db, session, choice=False):
        self.session = session
        self.db = db
        if choice:
            # self.__add_chronic_diseases()
            # self.__add_allergies()
            self.__add_fake_doctors(5)
            self.__add_fake_patients(10)
            self.__add_fake_consultations(10)

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
            information_sheet = InformationSheet(patient_id=patient.id)
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
                for chronic_disease in self.db.get_all_chronic_diseases():
                    if len(information_sheet.medical_history) > 3:
                        break
                    choice = random.choice([True, False])
                    if choice:
                        information_sheet.medical_history.append(chronic_disease)
            choice = random.choice([True, False])
            if choice:
                for allergy in self.db.get_all_allergies():
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
            self.db.add_entity(patient)
            self.db.add_entity(information_sheet)
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
            self.db.add_entity(doctor)
        self.db.save_to_database()

    def __add_fake_consultations(self, n):
        for i in range(n):
            patient_id = random.choice(self.get_all_patients()).id
            doctor_id = random.choice(self.get_all_doctors()).id
            time = self.__random_date(date(2015, 1, 1), datetime.now().date())
            pdf = randint(100, 1000 - 1)
            urgency_grade = randint(1, 5)
            consultation = Consultation(patient_id=patient_id, doctor_id=doctor_id, time=time, pdf=pdf,
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
        if (register_data[USERNAME_DOCTOR] == "" or register_data[PASSWORD_DOCTOR] == "" or register_data[
            FIRST_NAME_DOCTOR] == "" or
                register_data[LAST_NAME_DOCTOR] == "" or
                register_data[EMAIL_DOCTOR] == "" or register_data[PHONE_NUMBER_DOCTOR] == "" or register_data[
                    ADDRESS_DOCTOR] == "" or
                register_data[BIRTH_DATE_DOCTOR] == "" or
                register_data[CONSULTATION_SCHEDULE_OFFICE_DOCTOR] == "" or register_data[
                    CONSULTATION_SCHEDULE_AWAY_DOCTOR] == "" or
                register_data[ASSISTANTS_SCHEDULE_DOCTOR] == "" or register_data[GENDER_DOCTOR] == ""):
            raise ValueError
        doctor.username = register_data[USERNAME_DOCTOR]
        doctor.first_name = register_data[FIRST_NAME_DOCTOR]
        doctor.last_name = register_data[LAST_NAME_DOCTOR]
        doctor.email = register_data[EMAIL_DOCTOR]
        doctor.phone_number = register_data[PHONE_NUMBER_DOCTOR]
        doctor.address = register_data[ADDRESS_DOCTOR]
        doctor.birth_date = register_data[BIRTH_DATE_DOCTOR]
        doctor.consultation_schedule_office = register_data[CONSULTATION_SCHEDULE_OFFICE_DOCTOR]
        doctor.consultation_schedule_away = register_data[CONSULTATION_SCHEDULE_AWAY_DOCTOR]
        doctor.assistants_schedule = register_data[ASSISTANTS_SCHEDULE_DOCTOR]
        doctor.set_password(register_data[PASSWORD_DOCTOR])
        doctor.gender = register_data[GENDER_DOCTOR]
        self.db.add_entity(doctor)

    def register_patient(self, register_data):
        patient = Patient()
        if (register_data[USERNAME_PATIENT] == "" or register_data[FIRST_NAME_PATIENT] == "" or register_data[
            LAST_NAME_PATIENT] == "" or
                register_data[EMAIL_PATIENT] == ""
                or register_data[PHONE_NUMBER_PATIENT] == "" or register_data[ADDRESS_PATIENT] == ""
                or register_data[MARITAL_STATUS_PATIENT] == "" or register_data[
                    PASSWORD_PATIENT] == "" or register_data[GENDER_PATIENT] == "" or register_data[ZIP_CODE_PATIENT] == ""
                or register_data[CITY_PATIENT] == "" or register_data[COUNTY_PATIENT] == "" or register_data[PASSPORT_ID_PATIENT] == ""
                 or register_data[BIRTH_DATE_PATIENT] == "" or register_data[OCCUPATION_PATIENT] == "" or register_data[INVITE_CODE_PATIENT] == ""):
            raise ValueError
        patient.username = register_data[USERNAME_PATIENT]
        patient.first_name = register_data[FIRST_NAME_PATIENT]
        patient.last_name = register_data[LAST_NAME_PATIENT]
        patient.email = register_data[EMAIL_PATIENT]
        patient.phone_number = register_data[PHONE_NUMBER_PATIENT]
        patient.address = register_data[ADDRESS_PATIENT]
        patient.postalcode = register_data[ZIP_CODE_PATIENT]
        patient.city = register_data[CITY_PATIENT]
        patient.state = register_data[COUNTY_PATIENT]
        patient.passport_id = register_data[PASSPORT_ID_PATIENT]
        patient.birth_date = register_data[BIRTH_DATE_PATIENT]
        patient.occupation = register_data[OCCUPATION_PATIENT]
        patient.invite_code = register_data[INVITE_CODE_PATIENT]
        patient.martial_status = register_data[MARITAL_STATUS_PATIENT]
        patient.set_password(register_data[PASSWORD_PATIENT])
        patient.gender = register_data[GENDER_PATIENT]
        self.db.add_entity(patient)

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

    @staticmethod
    def generate_random_code():
        n = 0
        for _ in range(7):
            k = random.randint(0, 9)
            n = n * 10 + k
        return n

    def send_welcome_email(self, email_patient, email_companie):
        sender_account = email_companie
        reciever_account = email_patient
        cod = self.generate_random_code()
        message = f"Subject: BUN VENIT IN CLINICA NOASTRA!!\n Ne bucuram ca ati ales servicile noastre.\nCodul dumneavoastra de autentificare este:{cod}"
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_account, "your_password")
            server.sendmail(sender_account, reciever_account, message)

    def send_welcome_sms(self, sender_number, destination_number):
        account_sid = "account_sid"  # gasim pe twilio
        auth_token = "auth_token"
        client = Client(account_sid, auth_token)
        cod = self.generate_random_code()
        message_body = f"Subject: BUN VENIT IN CLINICA NOASTRA!!\n Ne bucuram ca ati ales servicile noastre.\nCodul dumneavoastra de autentificare este:{cod}"
        destination_number = "+04" + destination_number
        client.messages.create(
            to=destination_number,
            from_=sender_number,
            body=message_body)

    @staticmethod
    def get_consultation_history(patient_id):
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient:
            return patient.consultations.all()
        else:
            return None

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
        self.db.save_to_database()

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

    @staticmethod
    def save_file(file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'], filename))

    @staticmethod
    def validate_medical_proof(filename, medic_name):
        text = extract_text(filename)
        is_medic = re.compile('{}'.format(medic_name),  re.IGNORECASE)
        medic_name_matches = is_medic.findall(text)
        if len(medic_name_matches) == 0:
            return False
        is_medical_degree = re.compile("Medical Degree",  re.IGNORECASE)
        medical_degree_matches = is_medical_degree.findall(text)
        if len(medical_degree_matches) == 0:
            return False
        is_university = re.compile("University",  re.IGNORECASE)
        university_matches = is_university.findall(text)
        if len(university_matches) == 0:
            return False
        return True

