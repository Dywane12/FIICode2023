import random
from datetime import date, timedelta, datetime

import names
from faker import Faker
from random import randint
from cnpgen import Cnp, Gender, Region
from app import Patient, Doctor, Consultation


class Service:
    def __init__(self, db, choice=False):
        self.db = db
        if choice:
            self.__add_fake_doctors(50)
            doctors_ids = self.db.get_all_doctors_ids()
            self.__add_fake_patients(100, doctors_ids)
            patients_ids = self.db.get_all_patients_ids()
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
            patient = Patient(username, first_name, last_name, phone_number, email,
                              address, id_series, id_number, str(cnp), birth_date, marital_status, gender,
                              medical_record_id, password_hash, doctor_id
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
