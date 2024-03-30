from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, StopValidation, NumberRange, EqualTo
from wtforms.widgets import CheckboxInput, ListWidget
from flask_login import current_user
from app.database import *
from enum import Enum

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password:', validators=[DataRequired()])
    new_password = PasswordField('New Password:', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password:', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Change Password')
    
class DeleteUserDataForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    submit = SubmitField('Delete All User Data')