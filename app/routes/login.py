# from app import app
from app import *
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request, Flask
from flask_login import login_user, logout_user, login_required, current_user
from app.routes.functions.mail import *
from app.routes.functions.user_content import * 
import sys

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    login_form = SignInForm()
    signup_form = SignUpForm()
    return render_template('login.html', login_form=login_form, signup_form=signup_form)

@app.route('/login/submit', methods = ['GET', 'POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']
    user = db.session.query(User).filter_by(email=email).first()
    
    if user is None or not user.check_password(password):
        print(f'Login failed with this email and password combination', file=sys.stderr)
        flash('An error occurred when trying to sign-in', 'success')
        return redirect(url_for('landing'))

    login_user(user)
    return redirect(url_for('home'))
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Read data from form fields
    user_name = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password_retype = request.form['passwordRetype']
        
    user = db.session.query(User).filter_by(email=email).first()
    
    if user is None:
        if password == password_retype:
            # Create new user object and add to database
            user = User(username=user_name,first_name=first_name, last_name=last_name, email=email, newuser = True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            user = db.session.query(User).filter_by(email=email).first()
            account_creation_notification(user)
            login_user(user)
            flash('Account Created!', 'success')
            
            return redirect(url_for('home'))
        
        else:
            flash('An error occurred when trying to sign-up', 'success')
            return redirect(url_for('landing'))

    else:
        # account already created with email.
        print(f'Error: Signup failed for user: {first_name} {last_name}', file=sys.stderr)
        print(f'Provided email: {email} is already being used for an account.', file=sys.stderr)
        flash('An error occurred when trying to sign-up', 'success')
        return redirect(url_for('landing'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('landing'))
