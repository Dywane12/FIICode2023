from app import app
from flask import Flask, render_template, redirect, url_for, request
from flask_login import current_user, login_user
from app.domain.entities import Login
from flask import LoginForm
from flask_login import logout_user


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            #Invalid username or password
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))