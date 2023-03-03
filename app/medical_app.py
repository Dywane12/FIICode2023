from app import app, db
from app.domain.entities import Patient, Doctor, Consultation
from app.repository.database import Database
from app.service.service import Service
from app.ui.routes import Routes

if __name__ == '__main__':
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Patient': Patient, 'Doctor': Doctor, 'Consultation': Consultation}


    app.run(debug=True)
    db_1 = Database(db)
    service = Service(db_1, choice=False)
    ui = Routes(service)
    ui.run_all_routes()

    # db_1.clear_patients_table()
    # db_1.clear_consultation_table()
    # db_1.clear_doctors_table()
