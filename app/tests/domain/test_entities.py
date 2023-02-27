from unittest import TestCase
from app.domain.entities import Patient, Doctor
from datetime import datetime


class TestPatient(TestCase):
    def setUp(self):
        self.patient = Patient('John', 'Doe', '123456789', 'johndoe@example.com', '123 Main St', '123456',
                               '1234567890123', datetime(1990, 1, 1), 'Married', 'Male', 'MR001', 1)

    def test_getters(self):
        self.assertEqual(self.patient.id, 1)
        self.assertEqual(self.patient.first_name, 'John')
        self.assertEqual(self.patient.last_name, 'Doe')
        self.assertEqual(self.patient.phone_number, '123456789')
        self.assertEqual(self.patient.email, 'johndoe@example.com')
        self.assertEqual(self.patient.address, '123 Main St')
        self.assertEqual(self.patient.id_series, '123456')
        self.assertEqual(self.patient.cnp, '1234567890123')
        self.assertEqual(self.patient.birth_date, datetime(1990, 1, 1))
        self.assertEqual(self.patient.marital_status, 'Married')
        self.assertEqual(self.patient.gender, 'Male')
        self.assertEqual(self.patient.medical_record_id, 'MR001')

    def test_setters(self):
        self.patient.first_name = 'Jane'
        self.assertEqual(self.patient.first_name, 'Jane')

        self.patient.last_name = 'Doe'
        self.assertEqual(self.patient.last_name, 'Doe')

        self.patient.phone_number = '987654321'
        self.assertEqual(self.patient.phone_number, '987654321')

        self.patient.email = 'janedoe@example.com'
        self.assertEqual(self.patient.email, 'janedoe@example.com')

        self.patient.address = '456 Elm St'
        self.assertEqual(self.patient.address, '456 Elm St')

        self.patient.id_series = '654321'
        self.assertEqual(self.patient.id_series, '654321')

        self.patient.cnp = '9876543210123'
        self.assertEqual(self.patient.cnp, '9876543210123')

        self.patient.birth_date = datetime(1995, 1, 1)
        self.assertEqual(self.patient.birth_date, datetime(1995, 1, 1))

        self.patient.marital_status = 'Single'
        self.assertEqual(self.patient.marital_status, 'Single')

        self.patient.gender = 'Female'
        self.assertEqual(self.patient.gender, 'Female')


class TestDoctor(TestCase):

    def setUp(self):
        self.doc = Doctor("John", "Doe", "555-1234", "jdoe@example.com", "123 Main St.", datetime(1980, 1, 1), "M", [], [], [], 1)

    def test_getter(self):
        self.assertEqual(self.doc.first_name, "John")
        self.assertEqual(self.doc.last_name, "Doe")
        self.assertEqual(self.doc.phone_number, "555-1234")
        self.assertEqual(self.doc.email, "jdoe@example.com")
        self.assertEqual(self.doc.address, "123 Main St.")
        self.assertEqual(self.doc.birth_date, datetime(1980, 1, 1))
        self.assertEqual(self.doc.gender, "M")
        self.assertEqual(self.doc.consultation_schedule_office, [])
        self.assertEqual(self.doc.consultation_schedule_away, [])
        self.assertEqual(self.doc.assistants_schedule, [])
        self.assertEqual(self.doc.id, 1)

    def test_setters(self):
        self.doc.first_name = "Jane"
        self.assertEqual(self.doc.first_name, "Jane")

        self.doc.last_name = "Smith"
        self.assertEqual(self.doc.last_name, "Smith")

        self.doc.phone_number = "555-4321"
        self.assertEqual(self.doc.phone_number, "555-4321")

        self.doc.email = "jsmith@example.com"
        self.assertEqual(self.doc.email, "jsmith@example.com")

        self.doc.address = "456 Oak St."
        self.assertEqual(self.doc.address, "456 Oak St.")

        self.doc.birth_date = datetime(1985, 1, 1)
        self.assertEqual(self.doc.birth_date, datetime(1985, 1, 1))

        self.doc.gender = "F"
        self.assertEqual(self.doc.gender, "F")

        self.doc.consultation_schedule_office = ["Mon 9:00-11:00", "Wed 14:00-16:00"]
        self.assertEqual(self.doc.consultation_schedule_office, ["Mon 9:00-11:00", "Wed 14:00-16:00"])

        self.doc.consultation_schedule_away = ["2023-03-01", "2023-03-02"]
        self.assertEqual(self.doc.consultation_schedule_away, ["2023-03-01", "2023-03-02"])

        self.doc.assistants_schedule = ["Mon 11:00-12:00", "Tue 10:00-11:00"]
        self.assertEqual(self.doc.assistants_schedule, ["Mon 11:00-12:00", "Tue 10:00-11:00"])



