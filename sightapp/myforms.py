from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,TextAreaField

from flask_wtf.file import FileField, FileAllowed,FileRequired

from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    name = StringField("Center Name: ", validators=[DataRequired(message='The center name is required')])
    phone = StringField("Phone: ", validators=[DataRequired(message='Phone number can not be empty')])
    price = StringField("Price: ", validators=[DataRequired(message='Price must be set')])
    cover = FileField("Cover Picture:",validators=[FileRequired(message='Cover picture is required'),FileAllowed(["jpg","png"],"Invalid File Format")])
    description = TextAreaField("Description")
    available = SelectField('Availability', choices=[('active', 'Active'), ('disabled', 'Disabled')])

    submit = SubmitField("Update Account")
