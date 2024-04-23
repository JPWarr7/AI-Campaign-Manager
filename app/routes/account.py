# from app import app
from app import *
from app.database import *
from app.forms import *
from app.forms import DeleteUserDataForm
from flask import render_template, redirect, send_from_directory, url_for, flash, request, Flask
from flask_login import login_user, logout_user, login_required, current_user
from app.routes.functions.mail import *
from app.routes.functions.user_content import * 
import sys

@app.route('/viewAccount', methods=['GET', 'POST'])
@login_required
def view_account():
    content = user_content(current_user.id)
    return render_template('viewAccount.html', content = content)

@app.route('/changePasswordForm')
@login_required
def get_change_password_form():
    form = ChangePasswordForm()
    return render_template('changePassword.html', form=form)

@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def change_password():     
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        new_password=form.new_password.data
        password_retype=form.password_retype.data
        
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
        return redirect(url_for('login'))
    
    flash('Failed to change password. Please check your input.', 'error')

@app.route('/deleteUserDataForm')
@login_required
def get_delete_user_data_form():
    form = DeleteUserDataForm()
    return render_template('deleteUserData.html', form=form)

@app.route('/deleteUserData', methods=['GET', 'POST'])
@login_required
def delete_user_data():
    form = DeleteUserDataForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        if current_user.email.strip().lower() == email.strip().lower():
            user.delete_user_data()
            return redirect(url_for('deleted_successfully'))
        else:
            flash('Failed to delete user data. Please check your input.', 'error')

    flash('Failed to delete user data. Please check your input.', 'error')

@app.route('/deletedSuccessfully')
def deleted_successfully():
    return render_template('dataDeletedSuccessfully.html', error="User with provided email does not exist.")