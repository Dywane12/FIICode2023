import datetime

from app.domain.entities import Doctor, Patient, Consultation, ChronicDisease, Allergy, Drinker, Smoker, \
    Hospitalization, InformationSheet


class Database:

    def __init__(self, db):
        self.db = db
        self.db.create_all()

    def add_entity(self, entity):
        self.db.session.add(entity)

    def find_doctor_by_id(self, doctor_id):
        doctor = self.db.session.get(Doctor, doctor_id)
        if doctor is None:
            raise ValueError("Doctor not found")
        return doctor

    def find_consultation_by_id(self, consultation_id):
        consultation = self.db.session.get(Consultation, consultation_id)
        if consultation is None:
            raise ValueError("Doctor not found")
        return consultation

    def find_patient_by_id(self, patient_id):
        patient = self.db.session.get(Patient, patient_id)
        if patient is None:
            raise ValueError("Doctor not found")
        return patient

    @staticmethod
    def find_all_doctors():
        return Doctor.query.all()

    @staticmethod
    def find_all_patients():
        return Patient.query.all()

    @staticmethod
    def find_all_consultations():
        return Consultation.query.all()

    def find_all_doctors_ids(self):
        ids = []
        for doctor in self.find_all_doctors():
            ids.append(doctor.id)
        return ids

    def find_all_patients_ids(self):
        ids = []
        for patient in self.find_all_patients():
            ids.append(patient.id)
        return ids

    def save_to_database(self):
        self.db.session.commit()

    def clear_patients_table(self):
        self.db.session.query(Patient).delete()
        self.db.session.commit()

    def clear_doctors_table(self):
        self.db.session.query(Doctor).delete()
        self.db.session.commit()

    def clear_consultation_table(self):
        self.db.session.query(Consultation).delete()
        self.db.session.commit()

    @staticmethod
    def find_doctor_username(username):
        """
                The function returns True if there is any existing doctor with the given username and False otherwise
                :param username: str
                :return: True/False
                """
        return Doctor.query.filter_by(username=username).first()

    @staticmethod
    def find_patient_username(username):
        """
        The function returns True if there is any existing patient with the given username and False otherwise
        :param username: str
        :return: True/False
        """
        return Patient.query.filter_by(username=username).first()

    def update_doctor(self, doctor_id, updated):
        pass

    @staticmethod
    def find_all_chronic_diseases():
        return ChronicDisease.query.all()

    @staticmethod
    def find_all_allergies():
        return Allergy.query.all()

    def clear_smoker_table(self):
        self.db.session.query(Smoker).delete()
        self.db.session.commit()

    def clear_drinker_table(self):
        self.db.session.query(Drinker).delete()
        self.db.session.commit()

    def clear_hospitalization_table(self):
        self.db.session.query(Hospitalization).delete()
        self.db.session.commit()

    def clear_information_sheet_table(self):
        self.db.session.query(InformationSheet).delete()
        self.db.session.commit()

    def remove_consultation(self, consultation_id):
        consultation = Consultation.query.filter_by(consultation_id)
        if consultation:
            self.db.session.commit()
