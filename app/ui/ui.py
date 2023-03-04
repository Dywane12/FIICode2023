from app import app, db
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user
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
        self.__home()
        self.__login()
        self.__choice()
        self.__medic_profil()
        self.__transfer_pacienti()
        self.__lista_pacienti()
        self.__invita_pacienti()
        self.__medic_home()
        self.__register_pacient()
        self.__register_medic()
        self.__register_page_pacient()
        self.__register_page_medic()
        self.__login_page()

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
        if current_user.is_authenticated:
            return redirect(url_for('medic_home'))
        error = None
        if request.method == 'POST':
            if service.check_existence_doctor_username(request.form['username']) == False :
                error = 'Date gresite. Incearca din nou.'
            else:

                return redirect(url_for('home'))
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
    @app.route('/medic-home')
    def medic_home():
        return render_template('principal-medic.html')

    @staticmethod
    @app.route('/lista-pacienti')
    def __lista_pacienti():
        doctor = db.session.get(Doctor, 13)
        patients = service.get_doctor_patients(doctor)
        # patients = db.find_all_doctors_ids()
        return render_template('lista-pacienti.html', patients=patients)

    @staticmethod
    @app.route('/transfer-pacienti')
    def __transfer_pacienti():
        return render_template('transfer-pacienti.html')

    @staticmethod
    @app.route('/invita-pacienti')
    def __invita_pacienti():
        return render_template('invita-pacienti.html')

    @staticmethod
    @app.route('/medic-profil')
    def __medic_profil():
        return render_template('medic-profil.html')
