from dotenv import load_dotenv
from os import getenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
EMAIL_USER = getenv("EMAIL_USER")
EMAIL_PASS = getenv("EMAIL_PASS")
DATABASE_URI = getenv("DATABASE_URI")

class Config:
    SECRET_KEY = SECRET_KEY

    # Database specific config
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail specific config
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = EMAIL_USER
    MAIL_PASSWORD = EMAIL_PASS

