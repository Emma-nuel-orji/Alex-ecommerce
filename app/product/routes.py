from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import db
from app.product.forms import ProductForm
from app.models import Blog, Product, Recommendation
from flask_login import current_user, login_required
from app.product.utils import save_picture

prod = Blueprint('product', __name__)


@prod.route('/productpost', methods=['GET', 'POST'])
@login_required
def productpost():
    global image_file
    form = ProductForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            image = picture_file
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        category = form.category.data
        desc = form.desc.data
        author = current_user
        product = Product(name=name, price=price, discount=discount, category=category, desc=desc, author=author, image=image)
        db.session.add(product)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin.home'))
    elif request.method == 'GET':
        image_file = url_for('static', filename='img/' + Blog.image)
        image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('admin/productpost.html', form=form, image_file=image_file)


@prod.route('/single_product', methods=['GET', 'POST'])
def single_product():
    product = Product.query.all()
    recommendation = Recommendation.query.all()
    return render_template('single_product.html', product=product, recommendation=recommendation)


@prod.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    product = Product.query.all()
    return render_template("product.html", product=product)


@prod.route("/productpost/<int:product_id>", methods=['GET', 'POST'])
def products(product_id):
    prod = Product.query.get_or_404(product_id)
    return render_template("single_product.html", prod=prod)

