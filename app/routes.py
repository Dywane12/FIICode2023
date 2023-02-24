from app import app
from flask import render_template


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login-register')
def login_register():
    return render_template('login-register.html')
