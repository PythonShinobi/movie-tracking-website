from flask_wtf import FlaskForm
from wtforms.validators import (
    DataRequired, 
    Email, 
    EqualTo, 
    Length
)
from wtforms import (
    PasswordField, 
    StringField, 
    SubmitField, 
    BooleanField
)


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


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Current Password", validators=[
        DataRequired()
    ])

    new_password = PasswordField("New Password", validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("new_password2", message="Passwords must match.")
        ]
    )

    new_password2 = PasswordField("Confirm New Password", validators=[
        DataRequired()
    ])

    submit = SubmitField("Update Password")


class DeleteAccountForm(FlaskForm):
    """Form used to permanently delete the authenticated
        user's account.
    """

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    confirm = BooleanField(
        """I understand that this action cannot be undone.""",
        validators=[DataRequired()]
    )

    submit = SubmitField("Delete Account")