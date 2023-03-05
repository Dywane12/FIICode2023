import flask
from sqlalchemy.sql.functions import user
from app import app, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from app.repository.database import Database
from app.service.service import Service
from app.domain.entities import Patient, Doctor, Consultation
from werkzeug.security import check_password_hash

with app.app_context():
    db_1 = Database(db)
    # db_1.clear_patients_table()
    # db_1.clear_consultation_table()
    # db_1.clear_doctors_table()
    service = Service(db_1, choice=False)


class Routes:

    def __init__(self):
        self.__run_all_routes()

    def __run_all_routes(self):
        self.home()
        self.login_page()
        self.choice()
        self.medic_profil()
        self.transfer_pacienti()
        self.lista_pacienti()
        self.invita_pacienti()
        self.medic_home()
        self.register_pacient()
        self.register_medic()
        self.register_page_pacient()
        self.register_page_medic()
        self.login_page()

    @staticmethod
    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('index.html')

    @staticmethod
    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @staticmethod
    @app.route('/register-medic')
    def register_page_medic():
        return render_template('register_medic.html')

    @staticmethod
    @app.route('/register-pacient')
    def register_page_pacient():
        return render_template('register_pacient.html')

    @staticmethod
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if current_user.is_authenticated:
            if service.check_existence_doctor_username(current_user.username):
                return redirect(url_for('medic_home'))
            else:
                return redirect(url_for('pacient_home'))
        if service.check_existence_doctor_username(request.form['username']):
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                doctor = Doctor.query.filter_by(username=username).first()
                if doctor is None:
                    error = 'Date gresite. Incearca din nou.'
                elif not check_password_hash(doctor.password_hash, password):
                    error = 'Date gresite. Incearca din nou.'
                else:
                    service.doctor = doctor
                    login_user(doctor)
                    flask.flash("Conectare cu succes")
                    return redirect(url_for('medic_home'))
        elif service.check_existence_patient_username(request.form['username']):

            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                patient = Patient.query.filter_by(username=username).first()
                if patient is None:
                    error = 'Date gresite. Incearca din nou.'
                elif not check_password_hash(patient.password_hash, password):
                    error = 'Date gresite. Incearca din nou.'
                else:
                    service.patient = patient
                    login_user(patient)
                    flask.flash("Conectare cu succes")
                    return redirect(url_for('medic_home'))
        else:
            error = 'Date gresite. Incearca din nou.'
        return render_template('login.html', error=error)

    @staticmethod
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @staticmethod
    @app.route('/register-medic', methods=['GET', 'POST'])
    def register_medic():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' and request.form['password'] != 'admin' \
                    and request.form['email'] != 'admin@admin.com':
                error = 'Date gresite. Incearca din nou.'
            else:
                return redirect(url_for('medic_home'))
        return render_template('register_medic.html', error=error)

    @staticmethod
    @app.route('/register-pacient', methods=['GET', 'POST'])
    def register_pacient():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' and request.form['password'] != 'admin' \
                    and request.form['email'] != 'admin@admin.com':
                error = 'Date gresite. Incearca din nou.'
            else:
                return redirect(url_for('home'))
        return render_template('register_pacient.html', error=error)

    @staticmethod
    @app.route('/choice')
    def choice():
        return render_template('choice.html')

    @staticmethod
    @app.route('/medic-home')
    def medic_home():
        return render_template('principal-medic.html')

    @staticmethod
    @app.route('/pacient-home')
    def pacient_home():
        return render_template('principal-pacient.html')

    @staticmethod
    @app.route('/lista-pacienti')
    def lista_pacienti():
        patients = service.get_doctor_patients()
        # patients = db.find_all_doctors_ids()
        return render_template('lista-pacienti.html', patients=patients)

    @staticmethod
    @app.route('/transfer-pacienti')
    def transfer_pacienti():
        return render_template('transfer-pacienti.html')

    @staticmethod
    @app.route('/invita-pacienti')
    def invita_pacienti():
        return render_template('invita-pacienti.html')

    @staticmethod
    @app.route('/medic-profil')
    def medic_profil():
        return render_template('medic-profil.html')

    @staticmethod
    @app.route('/invita-pacienti', methods=['GET', 'POST'])
    def invitatie():
        error = None
        if request.method == 'POST':
            if request.form['email'] == 'admin@admin.com' and request.form['phone_number'] == '0722123123':
                message = 'Invitatia a fost trimisa!'
                return render_template('invita-pacienti.html', message=message)
            else:
                error = 'Date gresite. Incearca din nou.'
                return render_template('invita-pacienti.html', error=error)
