from flask import Flask
from dotenv import load_dotenv
from os import getenv, path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from .config import Config

load_dotenv()
DB_NAME = getenv("DB_NAME")

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app) 

    from .routes.views import views
    from .routes.auth import auth
    from .routes.errors import errors

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")

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

