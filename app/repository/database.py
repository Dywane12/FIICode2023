from app import Doctor, Patient, Consultation
from werkzeug.security import generate_password_hash, check_password_hash

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

    def save_to_database(self):
        self.db.session.commit()

    def generate_password_hash(self, password):
        self.db.session.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.db.session.password_hash, password)

    class Login(UserMixin, db.Model):
        @login.user_loader
        def load_user(id):
            return User.query.get(int(id))