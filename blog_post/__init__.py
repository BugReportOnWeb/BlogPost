from flask import Flask
from dotenv import load_dotenv
from os import getenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    return app

