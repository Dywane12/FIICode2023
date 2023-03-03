from app import app, db
from flask import Flask, render_template, redirect, url_for, request
from app.repository.database import Database
from app.service.service import Service
with app.app_context():
    db_1 = Database(db)
    service = Service(db_1, choice=False)


class Routes:

    def __init__(self):
        self.run_all_routes()

    def run_all_routes(self):
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
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' and request.form['password'] != 'admin':
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
    def lista_pacienti():
        service.get_all
        return render_template('lista-pacienti.html')

    @staticmethod
    @app.route('/transfer-pacienti')
    def transfer_pacienti():
        return render_template('transfer-pacienti.html')

    @staticmethod
    @app.route('/invita-pacienti')
    def invita_pacienti():
        return render_template('invita-pacienti.html')

    @app.route('/medic-profil')
    def medic_profil():
        return render_template('medic-profil.html')
