from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Blog, Gallery
from app.blogs.forms import BlogForm, GalleryForm, ProductForm, RecommendationForm
from app.blogs.utils import save_picture

blogs = Blueprint('blogs', __name__)


@blogs.route('/blogpost', methods=['GET', 'POST'])
def blogpost():
    global image_file
    form = BlogForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            image = picture_file
        title = form.title.data
        content = form.content.data
        author = current_user
        post = Blog(title=title, content=content, author=author, image=image)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        image_file = url_for('static', filename='img/' + Blog.image)
        image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('admin/blogpost.html', form=form, image_file=image_file)


@blogs.route('/image', methods=['GET', 'POST'])
@login_required
def image():
    global image_file
    form = GalleryForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            image = picture_file
        title = form.title.data
        content = form.content.data
        author = current_user
        gallery = Gallery(title=title, content=content, author=author, image=image)
        db.session.add(gallery)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        image_file = url_for('static', filename='img/' + Blog.image)
        image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('admin/image.html', form=form, image_file=image_file)


@blogs.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    posts = Blog.query.all()
    return render_template("blog.html", posts=posts)


@blogs.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    gallery = Gallery.query.all()
    return render_template("gallery.html", gallery=gallery)
