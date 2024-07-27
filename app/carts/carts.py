from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session, current_app
from flask_login import current_user, login_required
from app.models import Product, Recommendation
import json

carts = Blueprint('carts', __name__)


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@carts.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        product = Product.query.filter_by(id=product_id).first()

        if product_id and request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount, 'image': product.image, }}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                     # print('This product is already in cart') ///we commented this out
                else:
                     session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                     return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@carts.route('/catalog', methods=['GET', 'POST'])
@login_required
def catalog():
    recommendation = Recommendation.query.all()
    return render_template("catalog.html", recommendation=recommendation)


@carts.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        flash(f'please {current_user.username} Your cart is empty, add product to your cart to access this page...', 'warning')
        return redirect(url_for('product.product'))
    subtotal = 0
    grandtotal = 0
    for key, product, in session['Shoppingcart'].items():
        discount = 0
        discount = (discount / 100) * float(product['price'])
        subtotal += float(product['price'])
        subtotal -= discount
        grandtotal = float("%.2f" % (subtotal))

    return render_template('cart.html', grandtotal=grandtotal)


@carts.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('main.index'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('carts.cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('carts.cart'))


@carts.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('main.index'))
    except Exception as e:
        print(e)
