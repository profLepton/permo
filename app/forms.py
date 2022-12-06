
from email import message
from lib2to3.pgen2.token import NAME
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp, InputRequired
from app.models import User
from flask_login import current_user

NAME_REGEX = "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$"

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ProfessorRegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Regexp(NAME_REGEX, message='Please use valid character for your name.')])
    lastName = StringField('Last Name', validators=[DataRequired(), Regexp(NAME_REGEX, message='Please use valid character for your name.')])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=
    [DataRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@uml+\.edu", 
    message="Use a .edu email please.") ])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class StudentRegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Regexp(NAME_REGEX, message='Please use valid character for your name.')])
    lastName = StringField('Last Name', validators=[DataRequired(), Regexp(NAME_REGEX, message='Please use valid character for your name.')])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=
    [DataRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@student.uml.edu", 
    message="Use a student.uml.edu email please.") ])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        


class EditProfileForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired(), Regexp(NAME_REGEX, message='Please use valid character for your name.')])
    lastName = StringField('Last Name', validators=[InputRequired(), Regexp(NAME_REGEX, message='Please use valid character for your name.')])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    location = StringField('Location', validators=[InputRequired()])
    submit = SubmitField('Save Changes')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class AddClassesForm(FlaskForm):
    class_name = StringField('Class Name')
    submit = SubmitField('Submit')

class MakeRequestForm(FlaskForm):
    message = StringField('message')
    submit = SubmitField('Submit')


class AddPN(FlaskForm):
    pn = StringField('Permission numbers')

class AddPermissionNumbers(FlaskForm):
    permission_numbers = StringField('Permission numbers')
    submit = SubmitField('Submit')
