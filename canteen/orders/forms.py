from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, FieldList, DateField, SelectField
from wtforms.validators import DataRequired

class OrderFormForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    date_expired = StringField("Expiration datetime str", validators=[DataRequired()])
    date_started = StringField("Starting datetime str", validators=[DataRequired()])

    monday1 = StringField("Monday option 1")
    monday2 = StringField("Monday option 2")
    monday3 = StringField("Monday option 3")

    tuesday1 = StringField("Tuesday option 1")
    tuesday2 = StringField("Tuesday option 2")
    tuesday3 = StringField("Tuesday option 3")

    wednesday1 = StringField("Wednesday option 1")
    wednesday2 = StringField("Wednesday option 2")
    wednesday3 = StringField("Wednesday option 3")

    thursday1 = StringField("Thursday option 1")
    thursday2 = StringField("Thursday option 2")
    thursday3 = StringField("Thursday option 3")

    friday1 = StringField("Friday option 1")
    friday2 = StringField("Friday option 2")
    friday3 = StringField("Friday option 3")

    monday = FieldList(StringField("Monday option"), min_entries=2)

    days = [monday1, monday2, monday3, tuesday1, tuesday2, tuesday3, wednesday1, wednesday2, wednesday3, friday1, friday2, friday3, friday1, friday2, friday3]

    submit = SubmitField('Post')

class OrderFormResponse(FlaskForm):
    monday = SelectField('Monday', coerce=str)
    tuesday = SelectField('Tuesday', coerce=str)
    wednesday = SelectField('Wednesday', coerce=str)
    thursday = SelectField('Thursday', coerce=str)
    friday = SelectField('Friday', coerce=str)

    submit = SubmitField('Complete order')