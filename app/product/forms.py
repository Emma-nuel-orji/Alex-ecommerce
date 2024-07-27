from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'])])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)])
    price = StringField('Discount Price', validators=[DataRequired()])
    discount = StringField('Main Price', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=20)])
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post ')


