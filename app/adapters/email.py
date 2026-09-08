from threading import Thread

from flask_mail import Message
from flask import render_template
from jinja2 import TemplateNotFound

from app.extensions import mail


def send_async_email(app, message) -> None:
    """Send an email from a background thread."""

    with app.app_context():
        mail.send(message)


def send_mail(
    app,
    to,
    subject,
    template,
    **kwargs
) -> None:
    """Create and send an email asynchronously"""

    # Create message object
    message = Message(
        subject=app.config["MAIL_SUBJECT_PREFIX"] + subject,
        sender=app.config["MAIL_SENDER"],
        recipients=[to]
    )

    try:
        message.body = render_template(f"{template}.txt", **kwargs)
    except TemplateNotFound:
        pass

    try:
        message.html = render_template(f"{template}.html", **kwargs)
    except TemplateNotFound:
        pass

    
    email_thread = Thread(
        target=send_async_email,
        args=(app, message),
        daemon=True
    )

    email_thread.start()

    return email_thread