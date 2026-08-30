from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    """Form used to register a new user."""

    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])

    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])

    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8)
    ])

    password_confirmation = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password")
    ])

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """Form used to login an already existing user."""

    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8)
    ])

    submit = SubmitField("Login")