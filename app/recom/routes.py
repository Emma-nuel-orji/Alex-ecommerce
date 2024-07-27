from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import db
from app.recom.forms import RecommendationForm
from app.models import Blog, Product, Recommendation
from flask_login import current_user, login_required
from app.recom.utils import save_picture

recom = Blueprint('recom', __name__)


@recom.route('/recom', methods=['GET', 'POST'])
def recommendation():
    global image_file
    form = RecommendationForm()
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
        recommendation = Recommendation(name=name, price=price, discount=discount, category=category, desc=desc,
                                        author=author,
                                        image=image)
        db.session.add(recommendation)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin.home'))
    elif request.method == 'GET':
        image_file = url_for('static', filename='img/' + Blog.image)
        image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('admin/recommendation.html', form=form, image_file=image_file)


@recom.route("/recom/<int:recommendation_id>", methods=['GET', 'POST'])
def recommendations(recommendation_id):
    rec = Recommendation.query.get_or_404(recommendation_id)
    return render_template("single_rec.html", rec=rec)


@recom.route("/delete_rec/<int:rec_id>/delete", methods=['GET', 'POST'])
def delete_rec(rec_id):
    rec = Recommendation.query.get_or_404(rec_id)
    if current_user.id != 2:
        abort(403)
    db.session.delete(rec)
    db.session.commit()
    flash("the recommended product has been deleted successfully", 'success')
    return redirect(url_for('admin.home'))
    return render_template("Admin/home.html", rec=rec)


@recom.route("/delete_prod/<int:prod_id>/delete", methods=['GET', 'POST'])
def delete_prod(prod_id):
    prod = Product.query.get_or_404(prod_id)
    if current_user.id != 2:
        abort(403)
    db.session.delete(prod)
    db.session.commit()
    flash("the product has been deleted successfully", 'success')
    return redirect(url_for('admin.home'))
    return render_template("Admin/home.html", prod=prod)

