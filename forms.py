
from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError('Please use a different name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    second_name = StringField('Second Name', validators=[Length(min=0, max=32)])
    country = StringField('Country', validators=[Length(min=0, max=32)])
    sex = StringField('Sex', validators=[Length(min=0, max=32)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Sex', validators=[Length(min=0, max=13)])
    submit = SubmitField('Submit')
