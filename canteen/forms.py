from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from canteen.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken. Please choose an new one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("User with this email already exists. Please sign In")

class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already taken. Please choose an new one")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("User with this email already exists. Please sign In")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class OrderFormForm(FlaskForm):
    starting_date = DateField("Starting date", validators=[DataRequired()])
    days = [[
        StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]),
        StringField('Meal choice 2', validators=[DataRequired()]),
        StringField("Meal choice 3", validators=[DataRequired()])
    ],
    [
        StringField("Meal choice 1", validators=[DataRequired()]),
        StringField("Meal choice 2", validators=[DataRequired()]),
        StringField("Meal choice 3", validators=[DataRequired()])
    ],
    [
        StringField("Meal choice 1", validators=[DataRequired()]),
        StringField("Meal choice 2", validators=[DataRequired()]),
        StringField("Meal choice 3", validators=[DataRequired()])
    ], 
    [
        StringField("Meal choice 1", validators=[DataRequired()]),
        StringField("Meal choice 2", validators=[DataRequired()]),
        StringField("Meal choice 3", validators=[DataRequired()])
    ],
    [
        StringField("Meal choice 1", validators=[DataRequired()]),
        StringField("Meal choice 2", validators=[DataRequired()]),
        StringField("Meal choice 3", validators=[DataRequired()])
    ]

    ]
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    submit = SubmitField('Save')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. Please register to create an account")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')







