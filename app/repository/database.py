from app.domain.entities import Doctor, Patient, Consultation


class Database:

    def __init__(self, db):
        self.__db = db
        self.__db.create_all()

    def add_entity(self, entity):
        self.__db.session.add(entity)

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
        self.__db.session.commit()

    def clear_patients_table(self):
        self.__db.session.query(Patient).delete()
        self.__db.session.commit()

    def clear_doctors_table(self):
        self.__db.session.query(Doctor).delete()
        self.__db.session.commit()

    def clear_consultation_table(self):
        self.__db.session.query(Consultation).delete()
        self.__db.session.commit()

    def find_entity_by_id(self, entity_id):
        entity = self.__db.query.filter_by(id=entity_id).first()
        if entity is None:
            return None
        else:
            return entity
