from flask import render_template, Blueprint, url_for, flash, redirect, request, abort, session, current_app, \
    make_response
from app.models import User, Product, Recommendation, Blog, Checkout
from app import db
from app.forms import CheckoutForm, ContactForm
from app import mail
from flask_mail import Message
from flask_login import current_user, login_required
import json
import pdfkit
import stripe
import secrets

main = Blueprint('main', __name__)

publishable_key = 'pk_test_51LsSTZIo0R5Gyt8Mim3vwte0jrXt378wpMlp2diEvHMViy5BApipWObHiuh6sfJo9Lsx6b9WDxqudhKm1IAHW6XU00PPXOfdB8'

stripe.api_key = 'sk_test_51LsSTZIo0R5Gyt8Mrn9IYB8F77kdlwzKoUTEFvOgtEP43bS0z1HUDYhlokv9YiX9Sh3WdGPI6hxQYEBq7gTmasUy00k1JNdoNj'

@main.route('/c', methods=['GET', 'POST'])
def maincart():
    return render_template("maincart.html",)

@main.route('/l', methods=['GET', 'POST'])
def mainl():
    return render_template("mainlogin.html",)

@main.route('/r', methods=['GET', 'POST'])
def mainr():
    return render_template("mainregister.html",)


@main.route('/', methods=['GET', 'POST'])
def index():
    product = Product.query.all()
    recommendation = Recommendation.query.all()
    posts = Blog.query.all()
    return render_template("mainproducts.html", product=product, recommendation=recommendation, posts=posts)


@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        flash(f'please {current_user.username} add product to your cart to access this page...', 'warning')
        return redirect(url_for('product.product'))
    form = CheckoutForm()
    if form.validate_on_submit():
        try:
            subtotal = 0
            grandtotal = 0
            invoice = secrets.token_hex(5)
            customer_id = current_user.id
            product = Checkout.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(
                Checkout.id.desc()).all()
            for key, product in session['Shoppingcart'].items():
                discount = 0
                discount = (discount / 100) * float(product['price'])

                subtotal += float(product['price'])
                subtotal -= discount

                grandtotal = float("%.2f" % (subtotal))
                user = Checkout(productsname=(product['name']), grandtotal=grandtotal, customer_id=current_user.id,
                                orders=session['Shoppingcart'], invoice=secrets.token_hex(5),
                                firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data,
                                phone=form.phone.data, country=form.country.data, city=form.city.data,
                                street=form.street.data, building=form.building.data, zip=form.zip.data,
                                date_created=form.date_created.data, description=form.description.data, )
            db.session.add(user)
            db.session.commit()
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('main.payment'))
        except Exception as e:
            print(e)
            flash('something went wrong while getting order', 'danger')
            return redirect(url_for('product.product'))

    subtotal = 0
    grandtotal = 0
    invoice = secrets.token_hex(5)
    customer_id = current_user.id
    customer = User.query.filter_by(id=customer_id).first()
    orders = Checkout.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(
        Checkout.id.desc()).all()
    for key, product in session['Shoppingcart'].items():
        discount = 0
        discount = (discount / 100) * float(product['price'])

        subtotal += float(product['price'])
        subtotal -= discount

        grandtotal = ("%.2f" % float(subtotal))

    return render_template('checkout.html', title='Register', invoice=invoice, customer=customer, orders=orders,
                           form=form, grandtotal=grandtotal, product=product)



@main.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if payment and request.method == "POST":
        return redirect(url_for('main.thanks'))

    subtotal = 0
    grandtotal = 0
    invoice = secrets.token_hex(5)
    customer_id = current_user.id
    for key, product in session['Shoppingcart'].items():
        discount = 0
        discount = (discount / 100) * float(product['price'])

        subtotal += float(product['price'])
        subtotal -= discount

        grandtotal = ("%.2f" % float(subtotal))

    return render_template('payments.html', grandtotal=grandtotal)


@main.route('/thanks')
@login_required
def thanks():
    return render_template('thank.html')


@main.route('/faq', methods=['GET', 'POST'])
@login_required
def faq():
    return render_template("faq.html")


@main.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    user = User
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(f'New Message from {current_user.username}', sender=f'{user.email}',
                      recipients=['eorji452@gmail.com'])
        msg.body = f"""
           Name :  {form.name.data}

           Email :  {form.contact_email.data}

           Subject :  {form.subject.data}

           Message :  {form.message.data}
           """
        mail.send(msg)
        flash('your message have been sent', 'success')
        return redirect(url_for('main.index'))
    return render_template('contact.html', title='contact Form', form=form)


@main.route('/get_pdf', methods=['GET', 'POST'])
@login_required
def get_pdf():
    if current_user.is_authenticated:
        invoice = secrets.token_hex(5)
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = User.query.filter_by(id=customer_id).first()
            orders = Checkout.query.filter_by(customer_id=customer_id).order_by(Checkout.id.desc()).first()
            for _key, product in session['Shoppingcart'].items():
                discount = 0
                discount = (discount / 100) * float(product['price'])
                subTotal += float(product['price'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = ("%.2f" % float(subTotal))

            rendered = render_template('pdf.html', invoice=invoice, tax=tax, grandTotal=grandTotal, customer=customer,
                                       orders=orders)
            pdf = rendered
            response = make_response(pdf)

            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'atteched; filename=' + invoice + '.pdf'
            return response
    return redirect(url_for('main.checkout'))
