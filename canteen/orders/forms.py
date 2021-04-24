from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, SelectField
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms.validators import DataRequired

class OrderFormForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date_expired = DateField("Expiration datetime str", validators=[DataRequired()])
    date_started = DateField("Starting datetime str", validators=[DataRequired()])

    submit = SubmitField('Post')

# creating multiple fields for each day of the week 
fields = {'monday1': 'Monday option 1', 'monday2': 'Monday option 2', 'monday3': 'Monday option 3',
'tuesday1': 'Tuesday option 1', 'tuesday2': 'Tuesday option 2', 'tuesday3': 'Tuesday option 3',
'wednesday1': 'Wednesday option 1', 'wednesday2': 'Wednesday option 2', 'wednesday3': 'Wednesday option 3',
'thursday1': 'Thursday option 1', 'thursday2': 'Thursday option 2', 'thursday3': 'Thursday option 3',
'friday1': 'Friday option 1', 'friday2': 'Friday option 2', 'friday3': 'Friday option 3'}

for key, value in fields.items():
    setattr(OrderFormForm, key, StringField(value))

class OrderFormResponse(FlaskForm):
    monday = SelectField('Monday', coerce=str, validators=[DataRequired()], validate_choice=False)
    tuesday = SelectField('Tuesday', coerce=str, validators=[DataRequired()], validate_choice=False)
    wednesday = SelectField('Wednesday', coerce=str, validators=[DataRequired()], validate_choice=False)
    thursday = SelectField('Thursday', coerce=str, validators=[DataRequired()], validate_choice=False)
    friday = SelectField('Friday', coerce=str, validators=[DataRequired()], validate_choice=False)

    submit = SubmitField('Complete order')