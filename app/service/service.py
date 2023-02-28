from faker import Faker
from random import randint
from cnpgen import Cnp, Gender, Region
from app import Patient


class Service:
    def __init__(self, db):
        self.db = db
        self.__add_fake_doctors(50)
        self.__add_fake_patients(100)
        self.__add_fake_consulations(300)

    def __add_fake_patients(self, n):
        fake = Faker()
        for i in range(n):
            first_name, last_name = fake.name().split()
            username = first_name + '_' + last_name + f'{randint(1,420)}'
            phone_number = fake.phone_number()
            email = first_name + '_' + last_name + f'{randint(1,420)}' + '@gmail.com'
            address = fake.address()
            id_series = 'MM'
            id_number = randint(100000,1000000)
            cnp = Cnp(Gender.F, date(1993, 3, 4), Region.Bucuresti)
            birth_date, marital_status, gender, medical_record_id, doctor_id
            patient = Patient(
            )
            self.db.add_entity(patient)
        self.db.save_to_database()

    def __add_fake_doctors(n):
        fake = Faker()
        for i in range(n):
            user = User(
                name=fake.name(),
                age=randint(18, 65),
                address=fake.address(),
                phone=fake.phone_number(),
                email=fake.email())
            db.session.add(user)
        db.session.commit()

    @staticmethod
    def __add_fake_consulations(n):
        fake = Faker()
        for i in range(n):
            user = User(
                name=fake.name(),
                age=randint(18, 65),
                address=fake.address(),
                phone=fake.phone_number(),
                email=fake.email())
            db.session.add(user)
        db.session.commit()
