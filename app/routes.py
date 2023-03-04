from app import app
from flask import Flask, render_template, redirect, url_for, request


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register-medic')
def register_page_medic():
    return render_template('register_medic.html')

@app.route('/register-pacient')
def register_page_pacient():
    return render_template('register_pacient.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'medic' and request.form['password'] == 'admin':
            return redirect(url_for('medic_home'))
        elif request.form['username'] == 'pacient' and request.form['password'] == 'admin':
            return redirect(url_for('pacient_home'))
        else:
            error = 'Date gresite. Incearca din nou.'
            return render_template('login.html', error = error)

@app.route('/register-medic', methods=['GET', 'POST'])
def register_medic():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin' and request.form['email'] != 'admin@admin.com':
            error = 'Date gresite. Incearca din nou.'
        else:
            return redirect(url_for('medic_home'))
    return render_template('register_medic.html', error = error)

@app.route('/register-pacient', methods=['GET', 'POST'])
def register_pacient():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin' and request.form['email'] != 'admin@admin.com':
            error = 'Date gresite. Incearca din nou.'
        else:
            return redirect(url_for('home'))
    return render_template('register_pacient.html', error = error)

@app.route('/choice')
def choice():
    return render_template('choice.html')

@app.route('/medic-home')
def medic_home():
    return render_template('principal-medic.html')

@app.route('/lista-pacienti')
def lista_pacienti():
    return render_template('lista-pacienti.html')

@app.route('/transfer-pacienti')
def transfer_pacienti():
    return render_template('transfer-pacienti.html')

@app.route('/invita-pacienti')
def invita_pacienti():
    return render_template('invita-pacienti.html')

@app.route('/medic-profil')
def medic_profil():
    return render_template('medic-profil.html')

@app.route('/pacient-home')
def pacient_home():
    return render_template('principal-pacient.html')


@app.route('/invita-pacienti', methods=['GET', 'POST'])
def invitatie():
    error = None
    if request.method == 'POST':
        if request.form['email'] == 'admin@admin.com' and request.form['phone_number'] == '0722123123':
            message = 'Invitatia a fost trimisa!'
            return render_template('invita-pacienti.html', message = message)
        else:
            error = 'Date gresite. Incearca din nou.'
            return render_template('invita-pacienti.html', error = error)

