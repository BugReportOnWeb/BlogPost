from flask import Flask
from dotenv import load_dotenv
from os import getenv, path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
EMAIL_USER = getenv("EMAIL_USER")
EMAIL_PASS = getenv("EMAIL_PASS")

db = SQLAlchemy()
mail = Mail()
DB_NAME = "site.db"

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY

    # Database specific config
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Mail specific config
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = EMAIL_USER
    app.config["MAIL_PASSWORD"] = EMAIL_PASS

    db.init_app(app)
    mail.init_app(app) 

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(id):
        if id != 'None':
            return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("blog_post/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database")

