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
            form_data = {'AIDS/HIV': request.form['AIDS/HIV'],
                         'Anemia': request.form['Anemia'],
                         'Anxiety': request.form['Anxiety'],
                         'Arthritis': request.form['Arthritis'],
                         'Artificial Heart Valve': request.form['Artificial Heart Valve'],
                         'Artificial Joint': request.form['Artificial Joint'],
                         'Asthma': request.form['Asthma'],
                         'Back Problems': request.form['Back Problems'],
                         'Bleeding Disorder': request.form['Bleeding Disorder'],
                         'Bipolar Disorder': request.form['Bipolar Disorder'],
                         'Bloot Clot/DVT': request.form['Bloot Clot/DVT'],
                         'Bypass Surgery': request.form['Bypass Surgery'],
                         'Cancer': request.form['Cancer'],
                         'Chemical Dependency': request.form['Chemical Dependency'],
                         'Chest Pain': request.form['Chest Pain'],
                         'Circulatory Problems': request.form['Circulatory Problems'],
                         'Depression': request.form['Depression'],
                         'Diabetes': request.form['Diabetes'],
                         'Emphysema': request.form['Emphysema'],
                         'Eye Problems': request.form['Eye Problems'],
                         'Fibromyalgia': request.form['Fibromyalgia'],
                         'Foot Cramps': request.form['Foot Cramps'],
                         'Gout': request.form['Gout'],
                         'Headaches': request.form['Headaches'],
                         'Heart Attack': request.form['Heart Attack'],
                         'Heart Murmur': request.form['Heart Murmur']}
            try:
                information_sheet_id = service.register_information_sheet_1(form_data,
                                                                            service.session['register_patient_id'],
                                                                            diseases)
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
            form_data = {'Heart Failure': request.form.get('Heart Failure'),
                         'Hemophilia': request.form.get('Hemophilia'),
                         'Hepatitis': request.form.get('Hepatitis'),
                         'High Blood Pressure': request.form.get('High Blood Pressure'),
                         'Kidney Problems': request.form.get('Kidney Problems'),
                         'Leg Cramps': request.form.get('Leg Cramps'),
                         'Liver Disease': request.form.get('Liver Disease'),
                         'Low Blood Pressure': request.form.get('Low Blood Pressure'),
                         'Mental Illness': request.form.get('Mental Illness'),
                         'Neuropathy': request.form.get('Neuropathy'),
                         'Pacemaker': request.form.get('Pacemaker'),
                         'Paralysis': request.form.get('Paralysis'),
                         'Phlebitis': request.form.get('Phlebitis'),
                         'Psoriasis': request.form.get('Psoriasis'),
                         'Rheumatic Fever': request.form.get('Rheumatic Fever'),
                         'Schizophrenia': request.form.get('Schizophrenia'),
                         'Shortness of Breath': request.form.get('Shortness of Breath'),
                         'Stroke': request.form.get('Stroke'),
                         'Thyroid Problems': request.form.get('Thyroid Problems'),
                         'Tuberculosis': request.form.get('Tuberculosis'),
                         'Ulcers (Stomach)': request.form.get('Ulcers (Stomach)'),
                         'Varicose Veins': request.form.get('Varicose Veins'),
                         'Weight loss(unexplained)': request.form.get('Weight loss(unexplained)'),
                         'Pregnant': request.form.get('Pregnant'),
                         'Breastfeeding': request.form.get('Breastfeeding')}
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
            form_data = {'Local anesthesia': request.form.get('Local anesthesia'),
                         'Aspirin': request.form.get('Aspirin'),
                         'Anti-Inflammatory': request.form.get('Anti-Inflammatory'),
                         'Penicillin': request.form.get('Penicillin'),
                         'Sulfa': request.form.get('Sulfa'),
                         'IVP dye': request.form.get('IVP dye'),
                         'Tetanus': request.form.get('Tetanus'),
                         'General anesthesia': request.form.get('General anesthesia'),
                         'Latex': request.form.get('Latex'),
                         'Tape/Adhesives': request.form.get('Tape/Adhesives'),
                         'Iodine': request.form.get('Iodine'),
                         'Betadine': request.form.get('Betadine'),
                         'Codeine': request.form.get('Codeine'),
                         'Steroids': request.form.get('Steroids')}
            try:
                service.register_information_sheet_3(form_data, service.session['information_sheet_id'], allergies)
            except ValueError as exception:
                error = exception
            else:

                return redirect(url_for('register_patient_5'))
        return render_template('register_patient_4.html', allergies=allergies, error=error)

    @staticmethod
    @app.route('/register-patient-5')
    def register_patient_5():
        error = None
        if request.method == 'POST':
            form_data = [request.form['weight'],
                         request.form['height'],
                         request.form['shoe_size'],
                         request.form['medications'],
                         request.form['hospitalization'],
                         request.form.get('smoking'),
                         request.form.get('drinking')]
            try:
                service.register_information_sheet_4(form_data, service.session['information_sheet_id'])
            except ValueError as exception:
                error = exception
            else:
                service.link_patient_to_information_sheet()
                service.update_database()
                service.session.pop('register_patient_id')
                service.session.pop('information_sheet_id')
                return redirect(url_for('login'))
        return render_template('register_patient_5.html', error=error)

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

    """@app.route('/transfer-patients')
    def transfer_patients():
        error = None
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        if request.method == 'POST':
            patient_id = request.form['patient_id']
            doctor_id = request.form['doctor_id']
            service.transfer_patient(patient_id, doctor_id)
            return redirect(url_for('transfer_patients'))
        patients = service.get_patients_that_want_to_transfer()
        doctors = service.get_all_doctors()
        return render_template('transfer-patients.html', patients=patients, doctors=doctors)"""

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
        error = None
        if "doctor" not in service.session:
            return redirect(url_for('home'))
        if request.method == "POST":
            doctor = service.get_doctor_by_id(service.session['doctor'])
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['birth_date'], request.form['consultation_schedule_office'],
                         request.form['consultation_schedule_away'],
                         request.form['assistants_schedule'], request.form['password'], request.form['gender'],
                         request.files['proof_of_medic'], request.form['zipcode'], request.form['city'],
                         request.form['county'],
                         request.files['profile_picture']]
            try:
                service.update_doctor_profile(doctor, form_data)
            except ValueError as exception:
                error = exception
            else:
                service.update_database()
        return render_template('edit-medic.html', error=error)

    @staticmethod
    @app.route('/edit-patient', methods=['GET', 'POST'])
    def edit_patient():
        error = None
        if "patient" not in service.session:
            return redirect(url_for('home'))
        if request.method == "POST":
            patient = service.get_patient_by_id(service.session['patient'])
            form_data = [request.form['username'], request.form['first_name'], request.form['last_name'],
                         request.form['email'], request.form['phone_number'], request.form['address'],
                         request.form['zipcode'], request.form['city'],
                         request.form['county'], request.form['passport_id'],
                         request.form['birth_date'], request.form['marital_status'],
                         request.form['gender'], request.form['occupation'], request.form['password'],
                         request.form['invite_code'], request.files['profile_picture']]
            try:
                service.update_patient_profile(patient, form_data)
            except ValueError as exception:
                error = exception
            else:
                service.update_database()
        return render_template('edit-patient.html', error=error)

    @staticmethod
    @app.route('/list-patient-profile')
    def list_patient_profile():
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
    def information_sheet_function():
        patient_id = service.session['patient']
        patient = service.get_patient_by_id(patient_id)
        information_sheet = service.get_information_sheet_by_patient_id(service.session['patient'])
        return render_template('information-sheet.html', patient=patient, information_sheet=information_sheet)
