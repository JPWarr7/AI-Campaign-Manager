from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, StopValidation, NumberRange, EqualTo
from wtforms.widgets import CheckboxInput, ListWidget
from enum import Enum

    
class AddCampaignForm(FlaskForm):
    campaign_name = StringField('Campaign Name: ', validators=[DataRequired()])
    links = StringField('Enter your links: ', validators=[DataRequired()])
    perspective = StringField('Enter your POV: ', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditCampaignForm(FlaskForm):
    campaign_name = StringField('Campaign Name: ')
    links = StringField('Enter your links: ')
    text_summarization = StringField('Enter your links: ')
    perspective = StringField('Enter your POV: ')
    text_generation = StringField('Campaign Name: ')
    image_prompt = StringField('Enter your POV: ')
    image_generation = StringField('Enter your POV: ')
    submit = SubmitField('Save')