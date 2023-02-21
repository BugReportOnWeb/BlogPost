from flask import Blueprint, render_template, url_for
from flask_login import login_required

views = Blueprint("views", __name__)

dummy_data = [
    {
        "author": "Dev",
        "title":  "Some post title",
        "content": "Some post description",
        "date": "The creation date"
    },
    {
        "author": "Udhbhav",
        "title":  "Some other post title",
        "content": "Some other post description",
        "date": "The new creation date"
    },
    {
        "author": "Aman",
        "title":  "Some another post title",
        "content": "Some another post description",
        "date": "The latest creation date"
    }
]


@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html", posts=dummy_data)


@views.route("/about")
def about():
    return render_template("about.html")


@views.route("/account")
@login_required
def account():
    return render_template("account.html")

