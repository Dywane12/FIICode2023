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
        if request.form['username'] != 'admin' and request.form['password'] != 'admin':
            error = 'Date gresite. Incearca din nou.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error = error)

@app.route('/register-medic', methods=['GET', 'POST'])
def register_medic():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin' and request.form['email'] != 'admin@admin.com':
            error = 'Date gresite. Incearca din nou.'
        else:
            return redirect(url_for('home'))
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
