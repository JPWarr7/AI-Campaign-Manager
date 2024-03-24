from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, StopValidation, NumberRange, EqualTo
from wtforms.widgets import CheckboxInput, ListWidget
from flask_login import current_user
from app.database import *
from enum import Enum

    
class AddCampaignForm(FlaskForm):
    campaign_name = StringField('Campaign Name: ', validators=[DataRequired()])
    links = StringField('Enter your links: ', validators=[DataRequired()])
    perspective = StringField('Perspective: ', validators=[DataRequired()])
    portfolio = SelectField('Select Portfolio:', validators=[DataRequired()]) 
    submit = SubmitField('Save')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolio.choices = [(portfolio.id, portfolio.name) for portfolio in Portfolio.query.filter_by(user_id=current_user.id).all()]



class EditCampaignForm(FlaskForm):
    campaign_name = StringField('Campaign Name: ')
    links = StringField('Enter your links: ')
    text_summarization = StringField('Enter your links: ')
    perspective = StringField('Enter your POV: ')
    text_generation = StringField('Campaign Name: ')
    image_prompt = StringField('Enter your POV: ')
    image_generation = StringField('Enter your POV: ')
    submit = SubmitField('Save')