from app import Doctor, Patient, Consultation


class Database:

    def __init__(self, db):
        self.db = db
        self.db.create_all()

    def add_entity(self, entity):
        self.db.session.add(entity)
        self.db.session.commit()

    @staticmethod
    def get_all_doctors():
        return Doctor.query.all()

    @staticmethod
    def get_all_patients():
        return Patient.query.all()

    @staticmethod
    def get_all_consultations():
        return Consultation.query.all()
