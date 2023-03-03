from app import app
from flask import render_template, redirect, url_for, request, views


class Routes:

    def __init__(self, service):
        self.__service = service

    def run_all_routes(self):
        self.home()
        self.choice()
        self.login_page()
        self.register_page_medic()
        self.register_page_pacient()
        self.login()
        self.register_medic()
        self.register_pacient()
        self.medic_home()
        self.invita_pacienti()
        self.lista_pacienti()
        self.transfer_pacienti()
        self.medic_profil()

    @app.route('/')
    @app.route('/home')
    def home(self):
        return render_template('index.html')

    @app.route('/login')
    def login_page(self):
        return render_template('login.html')

    @app.route('/register-medic')
    def register_page_medic(self):
        return render_template('register_medic.html')

    @app.route('/register-pacient')
    def register_page_pacient(self):
        return render_template('register_pacient.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' and request.form['password'] != 'admin':
                error = 'Date gresite. Incearca din nou.'
            else:
                return redirect(url_for('home'))
        return render_template('login.html', error=error)

    @app.route('/register-medic', methods=['GET', 'POST'])
    def register_medic(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' and request.form['password'] != 'admin' and\
                    request.form['email'] != 'admin@admin.com':
                error = 'Date gresite. Incearca din nou.'
            else:
                return redirect(url_for('medic_home'))
        return render_template('register_medic.html', error=error)

    @app.route('/register-pacient', methods=['GET', 'POST'])
    def register_pacient(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' and request.form['password'] != 'admin'\
                    and request.form['email'] != 'admin@admin.com':
                error = 'Date gresite. Incearca din nou.'
            else:
                return redirect(url_for('home'))
        return render_template('register_pacient.html', error=error)

    @app.route('/choice')
    def choice(self):
        return render_template('choice.html')

    @app.route('/medic-home')
    def medic_home(self):
        return render_template('principal-medic.html')

    @app.route('/lista-pacienti')
    def lista_pacienti(self):
        return render_template('lista-pacienti.html')

    @app.route('/transfer-pacienti')
    def transfer_pacienti(self):
        return render_template('transfer-pacienti.html')

    @app.route('/invita-pacienti')
    def invita_pacienti(self):
        return render_template('invita-pacienti.html')

    @app.route('/medic-profil')
    def medic_profil(self):
        return render_template('medic-profil.html')
