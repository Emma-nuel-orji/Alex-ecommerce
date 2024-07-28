from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app.models import Checkout
from flask_login import current_user, login_required

from app import db
order = Blueprint('order', __name__)


@order.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    checkout = Checkout.query.all()
    return render_template('orders.html', checkout=checkout)


@order.route("/delete_order/<int:order_id>/delete", methods=['GET', 'POST'])
def delete_order(order_id):
    order = Checkout.query.get_or_404(order_id)
    if current_user.email != 'sativatrendy@gmail.com':
        abort(403)
    db.session.delete(order)
    db.session.commit()
    flash("the product has been deleted successfully", 'success')
    return redirect(url_for('admin.home'))
    return render_template("home.html", order=order)

