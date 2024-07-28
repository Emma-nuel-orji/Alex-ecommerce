from flask import render_template, url_for, flash, redirect, Blueprint

from app.models import User, Gallery, Product, Recommendation, Checkout
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__)


@admin.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    users = User.query.all()
    gallery = Gallery.query.all()
    product = Product.query.all()
    checkout = Checkout.query.all()
    recommendation = Recommendation.query.all()
    if current_user.email != 'sativatrendy@gmail.com':
        flash('Please you cant access to this page', 'danger')
        return redirect(url_for('index', users=users, gallery=gallery, product=product, recommendation=recommendation, checkout=checkout))
    else:
        render_template('home.html', users=users, gallery=gallery, product=product, recommendation=recommendation, checkout=checkout)
    return render_template("home.html", users=users, gallery=gallery, product=product,
                           recommendation=recommendation, checkout=checkout)
