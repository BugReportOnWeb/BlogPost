from flask import Blueprint, render_template, url_for, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import UpdateAccountForm
from . import db

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


@views.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash("You account has been updated!", category="success")
        return redirect(url_for("views.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", image_file=image_file, form=form)

