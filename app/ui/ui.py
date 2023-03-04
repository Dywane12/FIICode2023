from sqlalchemy.sql.functions import user
from app import app, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required
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
        self.login()
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
        """if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            doctor = Doctor.query.filter_by(username=form.username.data).first()
            if doctor is None:
                patient = Patient.query.filter_by(username=form.username.data).first()
                if patient is None or not patient.check_password(form.password.data):
                    flash('Date gresite. Incearca din nou.')
                    return redirect(url_for('login'))
            elif doctor.check_password(form.password.data):
                flash('Date gresite. Incearca din nou.')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))"""
        error = None
        if service.check_existence_doctor_username(request.form['username']):
            if current_user.is_authenticated:
                return redirect(url_for('medic_home'))
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
                    return redirect(url_for('medic_home'))
        elif service.check_existence_patient_username(request.form['username']):
            if current_user.is_authenticated:
                return redirect(url_for('patient_home'))
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
                    return redirect(url_for('medic_home'))
        else:
            error = 'Date gresite. Incearca din nou.'
        return render_template('login.html', error=error)

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
    @login_required
    @app.route('/medic-home')
    def medic_home():
        return render_template('principal-medic.html')

    @staticmethod
    @login_required
    @app.route('/lista-pacienti')
    def lista_pacienti():
        patients = service.get_doctor_patients()
        # patients = db.find_all_doctors_ids()
        return render_template('lista-pacienti.html', patients=patients)

    @staticmethod
    @login_required
    @app.route('/transfer-pacienti')
    def transfer_pacienti():
        return render_template('transfer-pacienti.html')

    @staticmethod
    @login_required
    @app.route('/invita-pacienti')
    def invita_pacienti():
        return render_template('invita-pacienti.html')

    @staticmethod
    @login_required
    @app.route('/medic-profil')
    def medic_profil():
        return render_template('medic-profil.html')
