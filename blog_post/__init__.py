from flask import Flask
from dotenv import load_dotenv
from os import getenv, path
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")

db = SQLAlchemy()
DB_NAME = "site.db"

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post

    create_database(app)

    return app


def create_database(app):
    if not path.exists("blog_post/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database")

