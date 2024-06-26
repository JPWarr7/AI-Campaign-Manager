# from app import app
from app import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from app.forms import *
from flask_login import login_user, logout_user, login_required, current_user
from app.routes.functions.user_content import *
from app import app

def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def landing():
    login_form = SignInForm()
    signup_form = SignUpForm()
    return render_template('landing.html',login_form=login_form, signup_form=signup_form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    content = user_content(current_user.id)
    return render_template('home.html', content = content)

@app.route('/privacypolicy')
def privacy_policy():
    return render_template('privacyPolicy.html')

@app.route('/termsofservice')
def terms_of_service():
    return render_template('termsOfService.html')

@app.route('/about')
def about():
    return render_template('about.html')