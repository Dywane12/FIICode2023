import random
from datetime import date, timedelta, datetime
import names
from faker import Faker
from random import randint
from cnpgen import Cnp, Gender, Region
from app.domain.entities import Patient, Doctor, Consultation

USERNAME = 0
FIRST_NAME = 1
LAST_NAME = 2
EMAIL = 3
PHONE_NUMBER = 4
ADDRESS = 5
BIRTH_DATE = 6
ID_SERIES = 6
ID_NUMBER = 7
CNP = 8
MARITAL_STATUS = 9
CONSULTATION_SCHEDULE_OFFICE = 7
CONSULTATION_SCHEDULE_AWAY = 8
ASSISTANTS_SCHEDULE = 9
PASSWORD = 10


class Service:
    def __init__(self, db, session, choice=False):
        self.session = session
        self.db = db
        if choice:
            self.__add_fake_doctors(50)
            doctors_ids = self.db.find_all_doctors_ids()
            self.__add_fake_patients(100, doctors_ids)
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
            password_hash = randint(10000000000, 100000000000 - 1)
            patient = Patient(username=username, first_name=first_name, last_name=last_name, phone_number=phone_number,
                              email=email, address=address, id_series=id_series, id_number=id_number, cnp=str(cnp),
                              birth_date=birth_date, marital_status=marital_status, gender=gender,
                              medical_record_id=medical_record_id, password_hash=password_hash, doctor_id=doctor_id
                              )
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
            password_hash = randint(10000000000, 100000000000 - 1)
            assistants_schedule = self.__random_schedule()
            doctor = Doctor(username, first_name, last_name, phone_number, email, address, birth_date, gender,
                            ', '.join(day for day in consultation_schedule_office),
                            ', '.join(day for day in consultation_schedule_away),
                            ' , '.join(day for day in assistants_schedule),
                            password_hash)
            self.db.add_entity(doctor)
        self.db.save_to_database()

    def __add_fake_consultations(self, n, patients_ids, doctors_ids):
        for i in range(n):
            patient_id = random.choice(patients_ids)
            doctor_id = random.choice(doctors_ids)
            time = f'{self.__random_date(date(2015, 1, 1), datetime.now().date())}'
            pdf = randint(100, 1000-1)
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
        end_hour = randint(start_hour+2, 18)
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
    def update_doctor_profile(doctor,update_data):
        if update_data[USERNAME] != "":
            doctor.username = update_data[USERNAME]
        if update_data[FIRST_NAME] != "":
            doctor.first_name = update_data[FIRST_NAME]
        if update_data[LAST_NAME] != "":
            doctor.last_name = update_data[LAST_NAME]
        if update_data[EMAIL] != "":
            doctor.email = update_data[EMAIL]
        if update_data[PHONE_NUMBER] != "":
            doctor.phone_number = update_data[PHONE_NUMBER]
        if update_data[ADDRESS] != "":
            doctor.address = update_data[ADDRESS]
        if update_data[BIRTH_DATE] != "":
            doctor.birth_date = update_data[BIRTH_DATE]
        if update_data[CONSULTATION_SCHEDULE_OFFICE] != "":
            doctor.consultation_schedule_office = update_data[CONSULTATION_SCHEDULE_OFFICE]
        if update_data[CONSULTATION_SCHEDULE_AWAY] != "":
            doctor.consultation_schedule_away = update_data[CONSULTATION_SCHEDULE_AWAY]
        if update_data[PASSWORD] != "":
            doctor.set_password(update_data[PASSWORD])

    @staticmethod
    def update_patient_profile(patient, update_data):
        if update_data[USERNAME] != "":
            patient.username = update_data[USERNAME]
        if update_data[FIRST_NAME] != "":
            patient.first_name = update_data[FIRST_NAME]
        if update_data[LAST_NAME] != "":
            patient.last_name = update_data[LAST_NAME]
        if update_data[EMAIL] != "":
            patient.email = update_data[EMAIL]
        if update_data[PHONE_NUMBER] != "":
            patient.phone_number = update_data[PHONE_NUMBER]
        if update_data[ADDRESS] != "":
            patient.address = update_data[ADDRESS]
        if update_data[ID_SERIES] != "":
            patient.id_series = update_data[ID_SERIES]
        if update_data[ID_NUMBER] != "":
            patient.id_number = update_data[ID_NUMBER]
        if update_data[CNP] != "":
            patient.cnp = update_data[CNP]
        if update_data[MARITAL_STATUS] != "":
            patient.martial_status = update_data[MARITAL_STATUS]
        if update_data[PASSWORD] != "":
            patient.set_password(update_data[PASSWORD])



