# from app import app
from app import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from app import *
from flask_login import login_user, logout_user, login_required, current_user
from app.routes.functions.user_content import *
from app import app

def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/devs')
def devs():
    return render_template('devs.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    content = user_content(current_user.id)
    return render_template('home.html', content = content)