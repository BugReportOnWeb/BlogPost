from flask import Blueprint, redirect, url_for, render_template

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html") 


@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))

