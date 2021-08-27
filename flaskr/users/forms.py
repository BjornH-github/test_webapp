from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flaskr.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired(), Length(min=4, max=20)]
    )
    email = StringField(
        'Email',
        validators=[InputRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[InputRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is taken. Please choose a different name')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email is taken. Please choose a different email address')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[InputRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')