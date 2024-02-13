from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, StopValidation, NumberRange, EqualTo
from wtforms.widgets import CheckboxInput, ListWidget
from enum import Enum

    
class newCampaignForm(FlaskForm):
    campaignName_Form = StringField('Campaign Name: ', validators=[DataRequired()])
    links_Form = StringField('Enter your links: ', validators=[DataRequired()])
    perspective_Form = StringField('Enter your POV: ', validators=[DataRequired()])
    submit = SubmitField('Save')


class UpdateCampaignForm(FlaskForm):
    campaign_name = StringField('Campaign Name: ', validators=[DataRequired()])
    links = StringField('Enter your links: ', validators=[DataRequired()])
    text_summarization = StringField('Enter your links: ', validators=[DataRequired()])
    perspective = StringField('Enter your POV: ', validators=[DataRequired()])
    text_generation = StringField('Campaign Name: ', validators=[DataRequired()])
    image_prompt = StringField('Enter your POV: ', validators=[DataRequired()])
    image_generation = StringField('Enter your POV: ', validators=[DataRequired()])
    submit = SubmitField('Save')