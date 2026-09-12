"""Authentication-related route decorators."""

from functools import wraps
from flask import redirect, url_for
from flask_login import current_user, login_required


def verified_required(view):
    """Require the current user to have a verified email address."""

    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if not current_user.user.email_verified:
            return redirect(url_for("auth.verify_required"))

        return view(*args, **kwargs)

    return wrapped_view