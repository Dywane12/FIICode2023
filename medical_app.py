
from app import app, db
from app.domain.entities import Patient, Doctor, Consultation
from app.repository.database import Database
from app.service.service import Service

if __name__ == '__main__':
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Patient': Patient, 'Doctor': Doctor, 'Consultation': Consultation}
    with app.app_context():
        db_1 = Database(db)
        service = Service(db_1, choice=True)
        #db_1.clear_patients_table()
        #db_1.clear_consultation_table()
        #db_1.clear_doctors_table()

    app.run()
