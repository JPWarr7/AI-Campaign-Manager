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
    return render_template('login.html')

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
    password_verification = request.form['password_verification']
        
    user = db.session.query(User).filter_by(email=email).first()
    
    if user is None:
        if password == password_verification:
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
        password_change_notification(user = db.session.query(User).filter_by(id=current_user.id))
        logout_user()
        return redirect(url_for('landing'))
    
    return redirect(url_for('index'))


@app.route('/delete_user_data', methods=['GET', 'POST'])
@login_required
def delete_user_data():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            user.delete_user_data()
            return redirect(url_for('deleted_successfully'))
        else:
            return render_template('deleteUserData.html', error="User with provided email does not exist.")
    content = user_content(current_user.id)
    return render_template('deleteUserData.html', content=content)

@app.route('/deleted_successfully')
def deleted_successfully():
    return render_template('dataDeletedSuccessfully.html', error="User with provided email does not exist.")

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacyPolicy.html')