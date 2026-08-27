import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base application configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY")

    PASSWORD_PEPPER = os.environ.get("PASSWORD_PEPPER")

    # Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(hours=1)
    REMEMBER_COOKIE_NAME = "remember_me_token"
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False

    # CSRF
    WTF_CSRF_TIME_LIMIT = 3600

    @staticmethod
    def init_app(app):
        """Perform application-specific initialization."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL") or f"sqlite:///{os.path.join(basedir, 'data-dev.sqlite')}"
    )

class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or f"sqlite:///{os.path.join(basedir, 'data-test.sqlite')}"
    )

class ProductionConfig(Config):
    """Prduction configuration."""

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("PROD_DATABASE_URL") or f"sqlite:///{os.path.join(basedir, 'data-prod.sqlite')}"
    )

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}