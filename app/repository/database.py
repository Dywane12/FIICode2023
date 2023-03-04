from app.domain.entities import Doctor, Patient, Consultation


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

    def find_doctor_username(self, username):
        """
                The function returns True if there is any existing doctor with the given username and False otherwise
                :param username: str
                :return: True/False
                """
        doctor = Doctor.query.filter_by(username=username).first()
        if doctor is not None and username == doctor.username:
            return True
        else:
            return False

    def find_patient_username(self, username):
        """
        The function returns True if there is any existing patient with the given username and False otherwise
        :param username: str
        :return: True/False
        """
        patient = Patient.query.filter_by(username=username).first()
        if patient is not None and username == patient.username:
            return True
        else:
            return False