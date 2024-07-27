from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField, \
    DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, length, equal_to
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exist please choose a different one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exist please choose a different one!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username already exist please choose a different one!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email already exist please choose a different one!')


class BlogForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class GalleryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Upload')


class ProductForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)])
    price = StringField('Discount Price', validators=[DataRequired()])
    discount = StringField('Main Price', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=20)])
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post ')


class RecommendationForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)])
    price = StringField('Discount Price', validators=[DataRequired()])
    discount = StringField('Main Price', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=20)])
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')


class CheckoutForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=2000)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=2000)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=2000)])
    city = StringField(validators=[DataRequired(), Length(min=2, max=2000)])
    street = StringField(validators=[DataRequired(), Length(min=2, max=2000)])
    building = StringField(validators=[DataRequired(), Length(min=2, max=2000)])
    zip = StringField(validators=[DataRequired(), Length(min=2, max=2000)])
    date_created = DateField(validators=[DataRequired()])
    description = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Confirm order')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), length(min=2, max=20)])
    contact_email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Mail')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(" There's no account with this email. Please register.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), equal_to('password')])
    submit = SubmitField('Reset Password')
