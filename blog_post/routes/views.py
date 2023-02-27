from flask import Blueprint, render_template, url_for, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from ..forms import UpdateAccountForm, PostForm
from .. import db
from ..models import Post, User
from PIL import Image, ImageOps
from io import BytesIO

import secrets
import os

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    page = request.args.get("page", 1, type=int);
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@views.route("/about")
def about():
    return render_template("about.html")


def save_picture(picture):
    random_hex = secrets.token_hex(8);
    _, file_extension = os.path.splitext(picture.filename) 
    picture_name = random_hex + file_extension
    picture_path = os.path.join(views.root_path, "static/profile_pics", picture_name)
    
    output_size = (125, 125)
    image = Image.open(picture)
    resized_image = ImageOps.exif_transpose(image)
    # Need some testing here b/w 'Image.resize' and 'Image.thumnail'
    resized_image.resize(output_size)

    resized_image.save(picture_path)

    return picture_name


@views.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            current_user.image_file = image_file

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


@views.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()

        flash("Your post has been created!", category="success")
        return redirect(url_for("views.home"))

    return render_template("create_post.html", form=form, legend_title="New Post")


@views.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@views.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if post.author != current_user:
        abort(403)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash("Your post has been updated!", category="success")
        return redirect(url_for("views.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", form=form, legend_title="Update Post")


@views.route("/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post) 
    db.session.commit()

    flash("Your post has been deleted!", category="success")
    return redirect(url_for("views.home"))


@views.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int);
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)

    return render_template("user_posts.html", posts=posts, user=user)

