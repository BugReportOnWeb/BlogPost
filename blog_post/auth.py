from flask import Blueprint, redirect, url_for, render_template, flash, request
from .forms import RegistrationForm, LoginForm
from .models import User, Post
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                flash("You have been logged in!", category="success")
                return redirect(next_page) if next_page else redirect(url_for("views.home"))
            else:
                flash("Password is incorrect.", category="danger")
        else:
            flash("Email is not registered.", category="danger")

    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        login_user(new_user)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Account created for {form.username.data}!", category="success")
        return redirect(url_for("views.home"))
        
    return render_template("register.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

