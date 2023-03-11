import random
import smtplib
from datetime import date, timedelta, datetime
import names
from faker import Faker
from random import randint
from cnpgen import Cnp, Gender, Region
from app.domain.entities import Patient, Doctor, Consultation
from twilio.rest import Client

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
BIRTH_DATE_PATIENT = 6
ID_SERIES_PATIENT = 6
ID_NUMBER_PATIENT= 7
CNP_PATIENT = 8
MARITAL_STATUS_PATIENT = 9
GENDER_PATIENT  = 10
MEDICAL_RECORD_ID_PATIENT = 11
PASSWORD_PATIENT = 12
INVITE_CODE_PATIENT = 13


class Service:
    def __init__(self, db, session, choice=False):
        self.session = session
        self.db = db
        if choice:
            self.__add_fake_doctors(25)
            doctors_ids = self.db.find_all_doctors_ids()
            self.__add_fake_patients(200, doctors_ids)
            patients_ids = self.db.find_all_patients_ids()
            self.__add_fake_consultations(300, patients_ids, doctors_ids)

    def __add_fake_patients(self, n, doctor_ids):
        fake = Faker()
        for i in range(n):
            gender = random.choice(['Male', 'Female'])
            first_name, last_name = names.get_full_name(gender=gender.lower()).split()
            username = first_name + '_' + last_name + f'{randint(1, 420)}'
            phone_number = fake.phone_number()
            email = first_name + '_' + last_name + f'{randint(1, 420)}' + '@gmail.com'
            address = fake.address()
            id_series = 'MM'
            id_number = randint(100000, 1000000 - 1)
            birth_date = self.__random_date(date(1940, 1, 1), date(2008, 12, 30))
            if gender == "Male":
                cnp = Cnp(Gender.M, birth_date, Region.Maramures)
            else:
                cnp = Cnp(Gender.F, birth_date, Region.Maramures)
            marital_status = random.choice(['Casatorit', 'Divortat', 'Vaduv', 'Necasatorit'])
            if gender == 'Female':
                marital_status += 'ă'
            medical_record_id = randint(100000, 1000000 - 1)
            doctor_id = random.choice(doctor_ids)
            password = 'nacho'

            patient = Patient(username=username, first_name=first_name, last_name=last_name, phone_number=phone_number,
                              email=email, address=address, id_series=id_series, id_number=id_number, cnp=str(cnp),
                              birth_date=birth_date, marital_status=marital_status, gender=gender,
                              medical_record_id=medical_record_id, doctor_id=doctor_id, occupation='Glovo delivery'
                              )
            patient.set_password(password)
            self.db.add_entity(patient)
        self.db.save_to_database()

    def __add_fake_doctors(self, n):
        fake = Faker()
        for i in range(n):
            gender = random.choice(['Male', 'Female'])
            first_name, last_name = names.get_full_name(gender=gender.lower()).split()
            username = first_name + '_' + last_name + f'{randint(1, 420)}'
            phone_number = fake.phone_number()
            email = first_name + '_' + last_name + f'{randint(1, 420)}' + '@gmail.com'
            address = fake.address()
            birth_date = self.__random_date(date(1960, 1, 1), date(1995, 12, 30))
            consultation_schedule_office = self.__random_schedule()
            consultation_schedule_away = consultation_schedule_office
            while consultation_schedule_office == consultation_schedule_away:
                consultation_schedule_away = self.__random_schedule()
            password = 'nacho'
            assistants_schedule = self.__random_schedule()
            doctor = Doctor(username=username, first_name=first_name, last_name=last_name, phone_number=phone_number,
                            email=email, address=address, birth_date=birth_date, gender=gender,
                            consultation_schedule_office=', '.join(day for day in consultation_schedule_office),
                            consultation_schedule_away=', '.join(day for day in consultation_schedule_away),
                            assistants_schedule=' , '.join(day for day in assistants_schedule))
            doctor.set_password(password)
            self.db.add_entity(doctor)
        self.db.save_to_database()

    def __add_fake_consultations(self, n, patients_ids, doctors_ids):
        for i in range(n):
            patient_id = random.choice(patients_ids)
            doctor_id = random.choice(doctors_ids)
            time = f'{self.__random_date(date(2015, 1, 1), datetime.now().date())}'
            pdf = randint(100, 1000 - 1)
            consultation = Consultation(patient_id, doctor_id, time, pdf)
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
        if (register_data[USERNAME_DOCTOR] == "" or register_data[PASSWORD_DOCTOR] == "" or register_data[FIRST_NAME_DOCTOR] == "" or
                register_data[LAST_NAME_DOCTOR] == "" or
                register_data[EMAIL_DOCTOR] == "" or register_data[PHONE_NUMBER_DOCTOR] == "" or register_data[ADDRESS_DOCTOR] == "" or
                register_data[BIRTH_DATE_DOCTOR] == "" or
                register_data[CONSULTATION_SCHEDULE_OFFICE_DOCTOR] == "" or register_data[CONSULTATION_SCHEDULE_AWAY_DOCTOR] == "" or
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
        if (register_data[USERNAME_PATIENT] == "" or register_data[FIRST_NAME_PATIENT] == "" or register_data[LAST_NAME_PATIENT] == "" or
                register_data[EMAIL_PATIENT] == ""
                or register_data[PHONE_NUMBER_PATIENT] == "" or register_data[ADDRESS_PATIENT] == "" or register_data[
                    ID_SERIES_PATIENT] == "" or register_data[ID_NUMBER_PATIENT] == ""
                or register_data[CNP_PATIENT] == "" or register_data[MARITAL_STATUS_PATIENT] == "" or register_data[PASSWORD_PATIENT] == ""
                or register_data[GENDER_PATIENT] == ""):
            raise ValueError
        patient.username = register_data[USERNAME_PATIENT]
        patient.first_name = register_data[FIRST_NAME_PATIENT]
        patient.last_name = register_data[LAST_NAME_PATIENT]
        patient.email = register_data[EMAIL_PATIENT]
        patient.phone_number = register_data[PHONE_NUMBER_PATIENT]
        patient.address = register_data[ADDRESS_PATIENT]
        patient.id_series = register_data[ID_SERIES_PATIENT]
        patient.id_number = register_data[ID_NUMBER_PATIENT]
        patient.cnp = register_data[CNP_PATIENT]
        patient.martial_status = register_data[MARITAL_STATUS_PATIENT]
        patient.medical_record_id = register_data[MEDICAL_RECORD_ID_PATIENT]
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
        if update_data[ID_SERIES_PATIENT] != "":
            patient.id_series = update_data[ID_SERIES_PATIENT]
        if update_data[ID_NUMBER_PATIENT] != "":
            patient.id_number = update_data[ID_NUMBER_PATIENT]
        if update_data[CNP_PATIENT] != "":
            patient.cnp = update_data[CNP_PATIENT]
        if update_data[MARITAL_STATUS_PATIENT] != "":
            patient.martial_status = update_data[MARITAL_STATUS_PATIENT]
        if update_data[PASSWORD_PATIENT] != "":
            patient.set_password(update_data[PASSWORD_PATIENT])

    def generate_random_code(self):
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

