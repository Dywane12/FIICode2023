from app import app
from flask import Flask, render_template, redirect, url_for, request


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login-register')
def login_register():
    return render_template('login-register.html')

@app.route('/login-register', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login-register.html', error = error)