from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired

class AddPortfolioForm(FlaskForm):
    portfolio_name = StringField('Portfolio Name: ', validators=[DataRequired()])
    description = StringField('Description')
    icon = FileField('Portfolio Icon', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Upload Portfolio Icon')])
    submit = SubmitField('Save')

class EditPortfolioForm(FlaskForm):
    portfolio_name = StringField('Portfolio Name: ')
    description = StringField('Description')
    icon = FileField('Portfolio Icon', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Upload Portfolio Icon')])
    submit = SubmitField('Save')
    