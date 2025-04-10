from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, NumberRange, EqualTo, Length

class AuditionForm(FlaskForm):
    name = StringField('Full Name*', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number*', validators=[DataRequired(), Length(min=10, max=15)])
    audition_type = SelectField('Audition For*', 
                              choices=[('', 'Select an option'), 
                                      ('Dancing', 'Dancing'),
                                      ('Acting', 'Acting'),
                                      ('Singing', 'Singing'),
                                      ('Other', 'Other')],
                              validators=[DataRequired()])
    age = IntegerField('Age* (Must be >18)', 
                      validators=[DataRequired(), 
                                 NumberRange(min=19, message="You must be older than 18")])
    submit = SubmitField('Submit')

class AdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), 
                                   EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Add Admin')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')