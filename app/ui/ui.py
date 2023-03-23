import os

import flask

from app import app, db
from flask import render_template, redirect, url_for, request, session, send_from_directory
from app.repository.database import Database
from app.service.service import Service
from werkzeug.security import check_password_hash
import datetime

with app.app_context():
    db_1 = Database(db)
    """db_1.clear_patients_table()
    db_1.clear_consultation_table()
    db_1.clear_doctors_table()
    db_1.clear_hospitalization_table()
    db_1.clear_drinker_table()
    db_1.clear_smoker_table()
    db_1.clear_information_sheet_table()
    db_1.clear_invite_code_table()"""
    service = Service(db_1, session, choice=False)


class Routes:

    def __init__(self):
        self.__run_all_routes()

    def __run_all_routes(self):
        self.home()
        self.choice()
        self.medic_profile()
        self.transfer_patients()
        self.patient_list()
        self.invite_patient()
        self.medic_home()
        self.register_patient()
        self.register_medic()
        self.register_page_patient()
        self.register_page_medic()
        self.login()

    @staticmethod
    @app.before_request
    def before_request():
        flask.session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=5)
        flask.session.modified = True

    @staticmethod
    @app.route('/clear-session', methods=['GET'])
    def clear_session():
        session.clear()
        return 'Session Cleared'

    @staticmethod
    @app.route('/')
    @app.route('/home')
    def home():
        if "doctor" in service.session:
            return redirect(url_for('medic_home'))
        elif "patient" in service.session:
            return redirect(url_for('patient_home'))
        return render_template('index.html')

    @staticmethod
    @app.route('/register-medic')
    def register_page_medic():
        return render_template('register_medic.html')

    @staticmethod
    @app.route('/register-patient')
    def register_page_patient():
        return render_template('register_patient.html')

    @staticmethod
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if "doctor" in service.session:
            return redirect(url_for('medic_home'))
        elif "patient" in service.session:
            return redirect(url_for('patient_home'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            doctor = service.get_doctor_by_username(str(username))
            patient = service.get_patient_by_username(str(username))
            if doctor is not None:
                if check_password_hash(doctor.password_hash, password):
                    service.session['doctor'] = doctor.id
                    return redirect(url_for('medic_home'))
                else:
                    error = 'Wrong password. Try again.'
            elif patient is not None:
                if not check_password_hash(patient.password_hash, password):
                    service.session['patient'] = patient.id
                    return redirect(url_for('patient_home'))
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
            service.session.pop('patient', None)
        return redirect(url_for('home'))

    @staticmethod
    @app.route('/register-medic', methods=['GET', 'POST'])
    def register_medic():
        error = None
        if request.method == 'POST':
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'],
                         request.form['consultation_schedule_away'],
                         request.form['assistants_schedule'], request.form['password'], request.form['gender'],
                         request.files['proof_of_medic'], request.form['zipcode'], request.form['city'],
                         request.form['county'],
                         request.files['profile_picture']]
            try:
                service.register_medic(form_data)
            except ValueError as exception:
                error = exception
            except AttributeError as exception:
                error = exception
            else:
                service.update_database()
                return redirect(url_for('home'))
        return render_template('register_medic.html', error=error)

    @staticmethod
    @app.route('/register-patient', methods=['GET', 'POST'])
    def register_patient():
        error = None
        if request.method == 'POST':
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['zipcode'], request.form['city'],
                         request.form['county'], request.form['passport_id'],
                         request.form['birth_date'], request.form['marital_status'],
                         request.form['gender'], request.form['occupation'], request.form['password'],
                         request.form['invite_code'], request.files['profile_picture']]
            try:
                patient_id = service.register_patient(form_data)
            except ValueError as exception:
                error = exception
            else:
                service.session['register_patient_id'] = patient_id
                return redirect(url_for('register_patient_2'))
        return render_template('register_patient.html', error=error)

    @staticmethod
    @app.route('/register-patient-2')
    def register_patient_2():
        error = None
        diseases = [{'name': 'AIDS/HIV', 'type': ''}, {'name': 'Anemia', 'type': ''}, {'name': 'Anxiety', 'type': ''},
                    {'name': 'Arthritis', 'type': 'Type'},
                    {'name': 'Artificial Heart Valve', 'type': ''}, {'name': 'Artificial Joint', 'type': ''},
                    {'name': 'Asthma', 'type': ''}, {'name': 'Back Problems', 'type': ''},
                    {'name': 'Bleeding Disorder', 'type': ''}, {'name': 'Bipolar Disorder', 'type': ''},
                    {'name': 'Bloot Clot/DVT', 'type': ''},
                    {'name': 'Bypass Surgery', 'type': ''},
                    {'name': 'Cancer', 'type': 'Type'}, {'name': 'Chemical Dependency', 'type': ''},
                    {'name': 'Chest Pain', 'type': ''}, {'name': 'Circulatory Problems', 'type': ''},
                    {'name': 'Depression', 'type': ''},
                    {'name': 'Diabetes', 'type': 'Type' 'How long'}, {'name': 'Emphysema', 'type': ''},
                    {'name': 'Eye Problems', 'type': ''}, {'name': 'Fibromyalgia', 'type': ''},
                    {'name': 'Foot Cramps', 'type': ''}, {'name': 'Gastric Reflux', 'type': ''},
                    {'name': 'Gout', 'type': ''}, {'name': 'Headaches', 'type': ''},
                    {'name': 'Heart Attack', 'type': ''}, {'name': 'Heart Murmur', 'type': ''},
                    ]
        if request.method == 'POST':
            form_data = [request.form['AIDS/HIV'], request.form['Anemia'], request.form['Anxiety'],
                         request.form['Arthritis'], request.form['Artificial Heart Valve'],
                         request.form['Artificial Joint'],
                         request.form['Asthma'], request.form['Back Problems'],
                         request.form['Bleeding Disorder'], request.form['Bipolar Disorder'],
                         request.form['Bloot Clot/DVT'], request.form['Bypass Surgery'],
                         request.form['Cancer'], request.form['Chemical Dependency'], request.form['Chest Pain'],
                         request.form['Circulatory Problems'], request.form['Depression'], request.form['Diabetes'],
                         request.form['Emphysema'], request.form['Eye Problems'], request.form['Fibromyalgia'],
                         request.form['Foot Cramps'],
                         request.form['Gout'], request.form['Headaches'], request.form['Heart Attack'],
                         request.form['Heart Murmur']]
            try:
                information_sheet_id = service.register_information_sheet_1(form_data, service.session['register_patient_id'], diseases)
            except ValueError as exception:
                error = exception
            else:
                service.session['information_sheet_id'] = information_sheet_id
                return redirect(url_for('register_patient_3'))
        return render_template('register_patient_2.html', diseases=diseases, error=error)

    @staticmethod
    @app.route('/register-patient-3')
    def register_patient_3():
        error = None
        diseases = [{'name': 'Heart Failure', 'type': ''}, {'name': 'Hemophilia', 'type': ''},
                    {'name': 'Hepatitis', 'type': ''}, {'name': 'High Blood Pressure', 'type': ''},
                    {'name': 'Kidney Problems', 'type': ''},
                    {'name': 'Leg Cramps', 'type': ''},
                    {'name': 'Liver Disease', 'type': ''}, {'name': 'Low Blood Pressure', 'type': ''},
                    {'name': 'Mental Illness', 'type': ''}, {'name': 'Neuropathy', 'type': ''},
                    {'name': 'Pacemaker', 'type': ''},
                    {'name': 'Paralysis', 'type': ''}, {'name': 'Phlebitis', 'type': ''},
                    {'name': 'Psoriasis', 'type': ''}, {'name': 'Rheumatic Fever', 'type': ''},
                    {'name': 'Schizophrenia', 'type': ''}, {'name': 'Shortness of Breath', 'type': ''},
                    {'name': 'Stroke', 'type': ''},
                    {'name': 'Thyroid Problems', 'type': 'Type'},
                    {'name': 'Tuberculosis', 'type': ''}, {'name': 'Ulcers (Stomach)', 'type': ''},
                    {'name': 'Varicose Veins', 'type': ''}, {'name': 'Weight loss(unexplained)', 'type': ''},
                    {'name': 'Pregnant?', 'type': ''}, {'name': 'Breastfeeding?', 'type': ''}
                    ]
        if request.method == 'POST':
            form_data = [request.form['Heart Failure'], request.form['Hemophilia'], request.form['Hepatitis'],
                         request.form['High Blood Pressure'], request.form['Kidney Problems'],
                         request.form['Leg Cramps'],
                         request.form['Liver Disease'], request.form['Low Blood Pressure'],
                         request.form['Mental Illness'], request.form['Neuropathy'],
                         request.form['Pacemaker'], request.form['Paralysis'],
                         request.form['Phlebitis'], request.form['Psoriasis'], request.form['Rheumatic Fever'],
                         request.form['Schizophrenia'], request.form['Shortness of Breath'], request.form['Stroke'],
                         request.form['Thyroid Problems'], request.form['Tuberculosis'],
                         request.form['Ulcers (Stomach)'], request.form['Varicose Veins'],
                         request.form['Weight loss(unexplained)'],
                         request.form['Pregnant'], request.form['Breastfeeding']]
            try:
                service.register_information_sheet_2(form_data, service.session['information_sheet_id'], diseases)
            except ValueError as exception:
                error = exception
            else:
                return redirect(url_for('register_patient_4'))
        return render_template('register_patient_3.html', diseases=diseases, error=error)

    @staticmethod
    @app.route('/register-patient-4')
    def register_patient_4():
        error = None
        allergies = [
            {'name': 'Local anesthesia'}, {'name': 'Aspirin'}, {'name': 'Anti-Inflammatory'}, {'name': 'Penicillin'},
            {'name': 'Sulfa'}, {'name': 'IVP dye'}, {'name': 'Tetanus'}, {'name': 'General anesthesia'},
            {'name': 'Latex'}, {'name': 'Tape/Adhesives'}, {'name': 'Iodine'}, {'name': 'Betadine'},
            {'name': 'Codeine'}, {'name': 'Steroids'}
        ]
        if request.method == 'POST':
            form_data = [request.form['Heart Failure'], request.form['Hemophilia'], request.form['Hepatitis'],
                         request.form['High Blood Pressure'], request.form['Kidney Problems'],
                         request.form['Leg Cramps'],
                         request.form['Liver Disease'], request.form['Low Blood Pressure'],
                         request.form['Mental Illness'], request.form['Neuropathy'],
                         request.form['Pacemaker'], request.form['Paralysis'],
                         request.form['Phlebitis'], request.form['Psoriasis'], request.form['Rheumatic Fever'],
                         request.form['Schizophrenia'], request.form['Shortness of Breath'],
                         request.form['Stroke'], request.form['Thyroid Problems'], request.form['Tuberculosis'],
                         request.form['Ulcers (Stomach)'], request.form['Varicose Veins'],
                         request.form['Weight loss(unexplained)'], request.form['Pregnant'],
                         request.form['Breastfeeding']]
            try:
                service.register_information_sheet_3(form_data, service.session['information_sheet_id'], allergies)
            except ValueError as exception:
                error = exception
            else:
                service.link_patient_to_information_sheet()
                service.update_database()
                service.session.pop('register_patient_id')
                service.session.pop('information_sheet_id')
                return redirect(url_for('login'))
        return render_template('register_patient_4.html', allergies=allergies, error=error)

    @staticmethod
    @app.route('/choice')
    def choice():
        return render_template('choice.html')

    @staticmethod
    @app.route('/medic-home')
    def medic_home():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        return render_template('medic-home.html')

    @staticmethod
    @app.route('/patient-home')
    def patient_home():
        if "patient" not in service.session:
            return redirect(url_for('home'))
        return render_template('patient-home.html')

    @staticmethod
    @app.route('/patient-list')
    def patient_list():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        patients = service.get_doctor_patients()
        # patients = db.find_all_doctors_ids()
        return render_template('patient-list.html', patients=patients)

    @staticmethod
    @app.route('/transfer-patients')
    def transfer_patients():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        return render_template('transfer-patients.html')

    @staticmethod
    @app.route('/invite-patient')
    def invite_patient():
        if "doctor" not in service.session:
            return redirect(url_for('home'))

        return render_template('invite-patient.html')

    @staticmethod
    @app.route('/medic-profile')
    def medic_profile():
        doctor = service.get_doctor_by_id(service.session['doctor'])
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        return render_template('medic-profile.html', doctor=doctor)

    @staticmethod
    @app.route('/patient-profile')
    def patient_profile():
        patient = service.get_patient_by_id(service.session['patient'])
        if "patient" not in service.session:
            return redirect(url_for('home'))
        return render_template('patient-profile.html', patient=patient)

    @staticmethod
    @app.route('/edit-medic', methods=['GET', 'POST'])
    def edit_medic():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        if request.method == "POST":
            doctor = service.get_doctor_by_id(service.session['doctor'])
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'],
                         request.form['consultation_schedule_away'],
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
        return render_template('list-patient-profile.html', doctor=doctor)

    @staticmethod
    @app.route('/consultation-history')
    def patient_medical_history():
        patient_id = service.session['patient']
        medical_history = service.get_consultation_history(patient_id)
        return render_template('medical-history.html', medical_history=medical_history)

    @staticmethod
    @app.route('/change-medic')
    def change_medic():
        patient_id = service.session['patient']
        patient = service.get_patient_by_id(patient_id)
        current_doctor = service.get_doctor_by_id(patient.doctor_id)
        doctors = service.get_doctors_nearby_patient(patient_id)
        return render_template('change-medic.html', current_doctor=current_doctor, doctors=doctors)

    @staticmethod
    @app.route('/consultations/<filename>')
    def uploaded_consultation(filename):
        return send_from_directory(os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], 'consultation')),
                                   filename)

    @staticmethod
    @app.route('/invite-patient', methods=['GET', 'POST'])
    def invitation():
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        email_companie = 'clinica_audi@gmail.com'
        email_patient = request.form['email']
        if request.method == 'POST':
            if email_patient == 'admin@admin.com':
                service.send_welcome_email(email_companie)
                message = 'Invite sent!'
                return render_template('invite-patient.html', message=message)
            else:
                error = 'Wrong credentials. Try again.'
                return render_template('invite-patient.html', error=error)

    @staticmethod
    @app.route('/information-sheet')
    def information_sheet():
        patient = service.get_patient_by_id(service.session['patient'])
        return render_template('information-sheet.html', patient=patient)

