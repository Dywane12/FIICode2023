from app import Doctor, Patient, Consultation


class Database:

    def __init__(self, db):
        self.db = db
        self.db.create_all()

    def add_entity(self, entity):
        self.db.session.add(entity)

    @staticmethod
    def get_all_doctors():
        return Doctor.query.all()

    @staticmethod
    def get_all_patients():
        return Patient.query.all()

    @staticmethod
    def get_all_consultations():
        return Consultation.query.all()

    def get_all_doctors_ids(self):
        ids = []
        for doctor in self.get_all_doctors():
            ids.append(doctor.id)
        return ids

    def get_all_patients_ids(self):
        ids = []
        for patient in self.get_all_patients():
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
