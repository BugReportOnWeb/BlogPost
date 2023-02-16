from flask import Blueprint, render_template, url_for

views = Blueprint("views", __name__)

dummy_data = [
    {
        "author": "Dev",
        "title":  "Some post tilte",
        "description": "Some post description",
        "date": "The creation date"
    },
    {
        "author": "Udhbhav",
        "title":  "Some other post tilte",
        "description": "Some other post description",
        "date": "The new creation date"
    },
    {
        "author": "Aman",
        "title":  "Some another post tilte",
        "description": "Some another post description",
        "date": "The latest creation date"
    }
]

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", posts=dummy_data)


@views.route("/about")
def about():
    return render_template("about.html")

