from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
            DataRequired(),
            Length(min=2, max=20) ])
    email = StringField("Email", validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
            DataRequired(),
            EqualTo("password")
        ])
    submit = SubmitField("Sign up")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already in use.")


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already in use.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[
            DataRequired(),
            Length(min=2, max=20)
        ])
    email = StringField("Email", validators=[
            DataRequired(),
            Email()
        ])
    picture = FileField("Update Profile Picture", validators=[
        FileAllowed(["png", "jpg", "jpeg"])
        ])
    submit = SubmitField("Update")


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already in use.")


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already in use.")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField("Request Password Reset")

    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("There is no account with that email. You must register first.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
            DataRequired(),
            EqualTo("password")
        ])
    submit = SubmitField("Reset Password")

