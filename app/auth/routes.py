"""HTTP routes for authentication."""

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
    fresh_login_required
)

from flask import (    
    url_for,
    redirect,
    render_template    
)

from app.extensions import db
from app.auth import auth as auth_blueprint
from app.adapters.repository import UserRepository
from app.adapters.password_hasher import PasswordHasher
from app.adapters.flask_login_user import FlaskLoginUser
from app.services.authentication import AuthenticationService
from app.auth.forms import (
    RegistrationForm, 
    LoginForm, 
    ChangePasswordForm
)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""

    form = RegistrationForm()

    if form.validate_on_submit():
        # Create the application service with the dependencies
        # required to perform user registration.
        service = AuthenticationService(
            repository=UserRepository(),
            password_hasher=PasswordHasher()
        )

        try:
            # Delegate the registration business workflow to the service.
            service.register(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
            )

            # Commit the pending database transaction after the service
            # has successfully completed the registration operation.
            db.session.commit()

        except ValueError as error:
            # The service rejected the registration because of a
            # business rule, such as an email that already exists.
            form.email.errors.append(str(error))

        # Execute this else block only if the try block finishes without raising an exception
        else:
            # Registration succeeded, so redirect to the login page.
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a user and create an authenticated session."""

    form = LoginForm()

    if form.validate_on_submit():
        # Create the application service with the dependencies
        # required to authenticate the user.
        service = AuthenticationService(
            repository=UserRepository(),
            password_hasher=PasswordHasher()
        )

        try:
            # Delegate credential verification to the application service.
            user = service.login(
                email=form.email.data,
                password=form.password.data
            )

        except ValueError as error:
            # The service rejected the credentials.
            form.email.errors.append(str(error))

        # Execute this else block only if the try block finishes without raising an exception
        else:
            # Authenticated succeeded, so create the user's
            # authenticated Flask-Login session.
            login_user(FlaskLoginUser(user))

            # Login succeeded, so redirect to the home page.
            return redirect(url_for("main.home")) 

    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
def logout():
    """Log out the currently authenticated user."""
    
    logout_user()
    return redirect(url_for("main.home"))


@auth_blueprint.route("/change-password", methods=["GET", "POST"])
@login_required
@fresh_login_required
def change_password():
    """Allow an authenticated user to change their password."""

    form = ChangePasswordForm()

    if form.validate_on_submit():
        service = AuthenticationService(
            repository=UserRepository(),
            password_hasher=PasswordHasher()
        )

        try:
            service.change_password(
                user=current_user.user,
                old_password=form.old_password.data,
                new_password=form.new_password.data
            )

            db.session.commit()
        
        except ValueError as error:
            form.old_password.errors.append(str(error))

        else:
            logout_user()
            return redirect(url_for("auth.login"))

    return render_template("auth/change_password.html", form=form)