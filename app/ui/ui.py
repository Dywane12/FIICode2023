from app import app, db
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user
from app.repository.database import Database
from app.service.service import Service
from werkzeug.security import check_password_hash

with app.app_context():
    db_1 = Database(db)
    # db_1.clear_patients_table()
    # db_1.clear_consultation_table()
    # db_1.clear_doctors_table()
    service = Service(db_1, session, choice=False)

class Routes:

    def __init__(self):
        self.__run_all_routes()

    def __run_all_routes(self):
        self.home()
        #self.login_page()
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
        self.login()

    @staticmethod
    @app.route('/')
    @app.route('/home')
    def home():
        if "doctor" in service.session:
            return redirect(url_for('medic_home'))
        elif "pacient" in service.session:
            return redirect(url_for('pacient_home'))
        return render_template('index.html')

    """@staticmethod
    @app.route('/login')
    def login_page():
        if "doctor" in service.session:
            flash("Deja logat")
            return redirect(url_for('medic_home'))
        elif "pacient" in service.session:
            flash("Deja logat")
            return redirect(url_for('pacient_home'))
        return render_template('login.html')"""

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
        if "doctor" in service.session:
            return redirect(url_for('medic_home'))
        elif "pacient" in service.session:
            return redirect(url_for('pacient_home'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            doctor = service.get_doctor_by_username(username)
            patient = service.get_patient_by_username(username)
            if doctor is not None:
                if check_password_hash(doctor.password_hash, password):
                    service.session['doctor'] = doctor.id
                    login_user(doctor)
                    return redirect(url_for('medic_home'))
                else:
                    error = 'Parola gresita. Incearca din nou.'
            elif patient is not None:
                if not check_password_hash(patient.password_hash, password):
                    service.session['pacient'] = patient.id
                    login_user(patient)
                    return redirect(url_for('pacient_home'))
                else:
                    error = 'Parola gresita. Incearca din nou.'
            else:
                error = 'Username nu exista. Incearca din nou.'
        return render_template('login.html', error=error)

    @staticmethod
    @app.route('/logout')
    def logout():
        if 'doctor' in service.session:
            service.session.pop('doctor', None)
        else:
            service.session.pop('pacient', None)
        logout_user()
        return redirect(url_for('login'))

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
        if "doctor" not in service.session:
            return redirect(url_for('login'))
        return render_template('principal-medic.html')

    @staticmethod
    @app.route('/pacient-home')
    def pacient_home():
        if "pacient" not in service.session:
            return redirect(url_for('login'))
        return render_template('principal-pacient.html')

    @staticmethod
    @app.route('/lista-pacienti')
    def lista_pacienti():
        if "doctor" not in service.session:
            return redirect(url_for('login'))
        patients = service.get_doctor_patients()
        # patients = db.find_all_doctors_ids()
        return render_template('lista-pacienti.html', patients=patients)

    @staticmethod
    @app.route('/transfer-pacienti')
    def transfer_pacienti():
        if "doctor" not in service.session:
            return redirect(url_for('login'))
        return render_template('transfer-pacienti.html')

    @staticmethod
    @app.route('/invita-pacienti')
    def invita_pacienti():
        if "doctor" not in service.session:
            return redirect(url_for('login'))
        return render_template('invita-pacienti.html')

    @staticmethod
    @app.route('/medic-profil')
    def medic_profil():
        doctor = service.get_doctor_by_id(service.session['doctor'])
        if "doctor" not in service.session:
            return redirect(url_for('login'))
        return render_template('medic-profil.html', doctor=doctor)

    @staticmethod
    @app.route('/invita-pacienti', methods=['GET', 'POST'])
    def invitatie():

        if request.method == 'POST':
            if email_patient == 'admin@admin.com' :
                service.send_welcome_email(email_companie, email_patient)
                message = 'Invitatia a fost trimisa!'
                return render_template('invita-pacienti.html', message=message)
            else:
                error = 'Date gresite. Incearca din nou.'
                return render_template('invita-pacienti.html', error=error)

    @staticmethod
    @app.route('/edit-medic', methods=['GET', 'POST'])
    def edit_medic():
        if request.method == "POST":
            doctor = service.get_doctor_by_id(service.session['doctor'])
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'], request.form['consultation_schedule_away'],
                         request.form['assistants_schedule'], request.form['password']]
            service.update_doctor_profile(doctor, form_data)
            service.update_database()
        return render_template('edit-medic.html')

    @staticmethod
    @app.route('/profil-lista-pacient')
    def profil_lista_pacient():
        doctor = service.get_doctor_by_id(service.session['doctor'])
        return render_template('profil-pacient-lista.html', doctor=doctor)
