# from app import app
from app import *
from app.database import *
from app.forms import *
from flask import render_template, redirect, send_from_directory, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import sys

@app.route('/login', methods = ['GET', 'POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    user = db.session.query(User).filter_by(email=email).first()
    
    if user is None or not user.check_password(password):
        print(f'Login failed for user: {user.first_name} {user.last_name}', file=sys.stderr)
        print(f'Provided email: {email}', file=sys.stderr)
        print(f'Provided password: {password}', file=sys.stderr)
        print(f'User object: {user}', file=sys.stderr)
        flash('An error occurred when trying to sign-in', 'success')
        return redirect(url_for('landing'))

    login_user(user)
    flash('Login Successful!', 'success')
    return redirect(url_for('index'))
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Read data from form fields
    user_name = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password_verification = request.form['password_verification']
        
    user = db.session.query(User).filter_by(email=email).first()
    
    if user is None:
        if password == password_verification:
            # Create new user object and add to database
            user = User(username=user_name,first_name=first_name, last_name=last_name, email=email, newuser = True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            print('Sign-up successful', file=sys.stderr)
            
            # email notification of sign-up
            # ACCT_EMAIL = email
            # try:
            #     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            #     server.login(EMAIL_USER, EMAIL_PASSWORD)

            #     body = f"Subject: Account Created\n\nWelcome to the Finance Tracker, {first_name} {last_name}! Your account information is listed below: \nName: {first_name} {last_name}\nEmail: {email}"
            #     server.sendmail(EMAIL_USER, ACCT_EMAIL, body)

            #     server.quit()
            
            # except Exception as e:
            #     return f"Error: {e}" 
            
            flash('Account Created!', 'success')
            return redirect(url_for('landing'))
        
        else:
            flash('An error occurred when trying to sign-up', 'success')
            return redirect(url_for('landing'))

    else:
        # account already created with email.
        print(f'Error: Signup failed for user: {first_name} {last_name}', file=sys.stderr)
        print(f'Provided email: {email} is already being used for an account.', file=sys.stderr)
        flash('An error occurred when trying to sign-up', 'success')
        return redirect(url_for('landing'))
    
# @app.route('/newuser', methods=['GET', 'POST'])
# @login_required
# def new_user():
#     if current_user.newuser == True:
#         print('new user.')
#     else:
#         print('not new user.')
    
#     return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('landing'))

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():     
    new_password = request.form['new_password']
    password_retype = request.form['password_retype']
        
    if new_password != password_retype:
        flash('Passwords do not match.', 'danger')
    else:
        new_password_hash = generate_password_hash(new_password)
        current_user.password = new_password_hash
        db.session.commit()
        flash('Your password has been updated. Please sign in again.', 'success')
        
        # Log user out after changing the password
        logout_user()
        return redirect(url_for('landing'))
    
    return redirect(url_for('index'))