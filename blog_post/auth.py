from flask import Blueprint, redirect, url_for, render_template, flash, request
from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from .models import User, Post
from . import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

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
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        flash(f"Account created for {form.username.data}!", category="success")
        return redirect(url_for("views.home"))
        
    return render_template("register.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message("Pasword Reset Request", sender="noreply@demo.com", recipients=[user.email])
    message.body = f'''To reset the password, visit the following link:
{url_for("auth.reset_password", token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
    '''
    mail.send(message)


@auth.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)

        flash("An email has been sent with instructions to reset your password", category="info")
        return redirect(url_for("auth.login"))

    return render_template("reset_request.html", form=form)


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    user = User.verify_reset_token(token)

    if not user:
        flash("This is an invalid or expired token", category="warning")
        return redirect(url_for("auth.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_hashed_password = generate_password_hash(form.password.data, method="sha256")
        user.password = new_hashed_password
        db.session.commit()

        flash("You password has been updated. You are now able to log in", category="success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)
