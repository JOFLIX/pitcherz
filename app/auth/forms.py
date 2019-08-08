from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField
from wtforms.validators import Required,Email,EqualTo
from ..models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User

class RegistrationForm(FlaskForm):
    """
    RegstrationForm class that passes in the required details for validation
    """

    email = StringField('your email address',validators=[Required(),Email()])
    username = StringField('your username',validators=[Required()])
    password = PasswordField('password',validators=[Required(),EqualTo('password',message='passwords must match')])
    password_confirm = PasswordField('confirm password',validators=[Required()])
    submit = SubmitField('sign Up')


    #custom validators
    def validate_email(self,data_field):
        '''
        Functions takes in the data field and checks our database to confirm user Validation
        '''
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('there is an account with that email')

    def validate_username(self,data_field):
        '''
        Function checks if the username is unique and raises ValidationError
        '''
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('that user name is already taken. Try another one')

#login class  takes three inputs from the user
class LoginForm(FlaskForm):
    email = StringField('your email address',validators=[Required(),Email()])
    password = PasswordField('password',validators=[Required()])
    remember = BooleanField('remember me')
    submit = SubmitField('sign in')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
