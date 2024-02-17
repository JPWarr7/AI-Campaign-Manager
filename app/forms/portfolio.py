from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddPortfolioForm(FlaskForm):
    portfolio_name = StringField('Portfolio Name: ', validators=[DataRequired()])
    submit = SubmitField('Save')

class EditPortfolioForm(FlaskForm):
    portfolio_name = StringField('Portfolio Name: ')
    submit = SubmitField('Save')
    