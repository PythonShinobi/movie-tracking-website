from app.adapters.email import send_mail


def test_send_mail(app):
    app.config["MAIL_SUPPRESS_SEND"] = True
    app.config["MAIL_SUBJECT_PREFIX"] = "[Movie Tracking] "
    app.config["MAIL_SENDER"] = "noreply@example.com"
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["PREFERRED_URL_SCHEME"] = "http"

    with app.app_context():
        thread = send_mail(
            to="john@example.com",
            subject="Verify your email",
            template="auth/email/verify_email",
            username="john",
            token="abc123",
        )

        thread.join()