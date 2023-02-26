
from app import app, db
from app.domain.entities import Patient, Doctor, Consultation


if __name__ == '__main__':
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Patient': Patient, 'Doctor': Doctor, 'Consultation': Consultation}
    with app.app_context():
        db.create_all()
    app.run()
