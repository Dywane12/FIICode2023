from app import app, db
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user
from app.repository.database import Database
from app.service.service import Service
from werkzeug.security import check_password_hash

with app.app_context():
    db_1 = Database(db)
    """db_1.clear_patients_table()
    db_1.clear_consultation_table()
    db_1.clear_doctors_table()"""
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
    @app.route('/register-patient-2')
    def register_patient_2():
        diseases = [{'name': 'AIDS/HIV', 'type': ''}, {'name': 'Anemia', 'type': ''}, {'name': 'Anxiety', 'type': ''}, {'name': 'Arthritis', 'type': 'Type'},
                    {'name': 'Artificial Heart Valve', 'type': ''}, {'name': 'Artificial Joint', 'type': ''},
                    {'name': 'Asthma', 'type': ''}, {'name': 'Back Problems', 'type': ''}, {'name': 'Bleeding Disorder', 'type': ''}, {'name': 'Bipolar Disorder', 'type': ''}, {'name': 'Bloot Clot/DVT', 'type': ''},
                    {'name': 'Bypass Surgery', 'type': ''},
                    {'name': 'Cancer', 'type': 'Type'}, {'name': 'Chemical Dependency', 'type': ''}, {'name': 'Chest Pain', 'type':''}, {'name': 'Circulatory Problems', 'type': ''}, {'name': 'Depression', 'type': ''},
                    {'name': 'Diabetes', 'type': 'Type' 'How long'}, {'name': 'Emphysema', 'type': ''},
                    {'name': 'Eye Problems', 'type': ''}, {'name': 'Fibromyalgia', 'type': ''}, {'name': 'Fott Cramps', 'type':''}, {'name': 'Gastric Reflux', 'type': ''}, {'name': 'Gout', 'type': ''}, {'name': 'Headaches', 'type': ''},
                    {'name': 'Heart Attack', 'type': ''}, {'name': 'Heart Murmur', 'type': ''},
                    {'name': 'Heart Failure', 'type': ''}, {'name': 'Hemophilia', 'type': ''}, {'name': 'Hepatitis', 'type':''}, {'name': 'High Blood Pressure', 'type': ''}, {'name': 'Kidney Problems', 'type': ''},
                    {'name': 'Leg Cramps', 'type': ''},
                    {'name': 'Liver Disease', 'type': ''}, {'name': 'Low Blood Pressure', 'type': ''}, {'name': 'Mental Illness', 'type': ''}, {'name':'Neuropathy', 'type': ''}, {'name': 'Pacemaker', 'type': ''},
                    {'name': 'Paralysis', 'type': ''}, {'name': 'Phlebitis', 'type' :''},
                    {'name': 'Psoriasis', 'type': ''}, {'name': 'Rheumatic Fever', 'type': ''}, {'name': 'Schizophrenia', 'type': ''}, {'name': 'Shortness of Breath', 'type': ''}, {'name': 'Stroke', 'type': ''},
                    {'name': 'Thyroid Problems', 'type': 'Type'},
                    {'name': 'Tuberculosis', 'type': ''}, {'name': 'Ulcers (Stomach)', 'type': ''}, {'name': 'Varicose Veins', 'type': ''}, {'name':'Wight loss, unexplained', 'type': ''},
                    {'name': 'Pregnant?', 'type': ''}, {'name': 'Breastfeeding?', 'type': ''}
                    ]
        return render_template('register_pacient_2.html', diseases=diseases)

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
                    error = 'Wrong password. Try again.'
            elif patient is not None:
                if not check_password_hash(patient.password_hash, password):
                    service.session['pacient'] = patient.id
                    login_user(patient)
                    return redirect(url_for('pacient_home'))
                else:
                    error = 'Wrong password. Try again.'
            else:
                error = 'The username does not exist. Try again.'
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
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'],
                         request.form['consultation_schedule_away'],
                         request.form['assistants_schedule'], request.form['password'], request.form['gender']]
            try:
                service.register_medic(form_data)
            except ValueError:
                error = "Invalid data. Try again"
            else:
                service.update_database()
                return redirect(url_for('home'))
        return render_template('register_medic.html', error=error)

    @staticmethod
    @app.route('/register-pacient', methods=['GET', 'POST'])
    def register_pacient():
        error = None
        if request.method == 'POST':
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['serie_buletin'],
                         request.form['number_buletin'],
                         request.form['cnp'], request.form['marital_status'], request.form['medical_record_id'],
                         request.form['gender'], request.form['password'], request.form['invite_code']]
            try:
                service.register_patient(form_data)
            except ValueError:
                error = "Invalid data. Try again"
            else:
                service.update_database()
                return redirect(url_for('regiser_patient_2'))
        return render_template('register_pacient.html', error=error)

    @staticmethod
    @app.route('/choice')
    def choice():
        return render_template('choice.html')

    @staticmethod
    @app.route('/medic-home')
    def medic_home():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        return render_template('principal-medic.html')

    @staticmethod
    @app.route('/pacient-home')
    def pacient_home():
        if "pacient" not in service.session:
            return redirect(url_for('home'))
        return render_template('principal-pacient.html')

    @staticmethod
    @app.route('/lista-pacienti')
    def lista_pacienti():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        patients = service.get_doctor_patients()
        # patients = db.find_all_doctors_ids()
        return render_template('lista-pacienti.html', patients=patients)

    @staticmethod
    @app.route('/transfer-pacienti')
    def transfer_pacienti():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        return render_template('transfer-pacienti.html')

    @staticmethod
    @app.route('/invita-pacienti')
    def invita_pacienti():
        if "doctor" not in service.session:
            return redirect(url_for('home'))

        return render_template('invita-pacienti.html')

    @staticmethod
    @app.route('/medic-profil')
    def medic_profil():
        doctor = service.get_doctor_by_id(service.session['doctor'])
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        return render_template('medic-profil.html', doctor=doctor)

    @staticmethod
    @app.route('/invita-pacienti', methods=['GET', 'POST'])
    def invitatie():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        error = None
        email_companie = 'clinica_audi@gmail.com'
        email_patient = request.form['email']
        if request.method == 'POST':
            if email_patient == 'admin@admin.com' :
                service.send_welcome_email(email_companie, email_patient)
                message = 'Invite sent!'
                return render_template('invita-pacienti.html', message=message)
            else:
                error = 'Wrong credentials. Try again.'
                return render_template('invita-pacienti.html', error=error)

    @staticmethod
    @app.route('/edit-medic', methods=['GET', 'POST'])
    def edit_medic():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        if request.method == "POST":
            doctor = service.get_doctor_by_id(service.session['doctor'])
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'], request.form['consultation_schedule_away'],
                         request.form['assistants_schedule'], request.form['password'], request.form['gender']]
            service.update_doctor_profile(doctor, form_data)
            service.update_database()
        return render_template('edit-medic.html')

    @staticmethod
    @app.route('/profil-lista-pacient')
    def profil_lista_pacient():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        doctor = service.get_doctor_by_id(service.session['doctor'])
        return render_template('profil-pacient-lista.html', doctor=doctor)

    @staticmethod
    @app.route('/medical-history')
    def patient_medical_history():
        patient_id = current_user.id
        medical_history = service.get_consultation_history(patient_id)
        return render_template('medical_history.html', medical_history=medical_history)