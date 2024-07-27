from app import db

from datetime import datetime


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.String(20), nullable=False, default='default.jpg.png')
#     name = db.Column(db.String(20), nullable=False)
#     price = db.Column(db.String, nullable=False)
#     discount = db.Column(db.String, nullable=False)
#     category = db.Column(db.String(20), nullable=False)
#     desc = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     def __repr__(self):
#         return '<Addproduct %r>' % self.name



#
# class Addproduct(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     price = db.Column(db.Numeric(10, 2), nullable=False)
#     discount = db.Column(db.Integer, default=0)
#     desc = db.Column(db.Text, nullable=False)
#     pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
#     brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))
#
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
#     category = db.relationship('Category', backref=db.backref('brands', lazy=True))
#
#     image = db.Column(db.String(150), nullable=False, default='image.jpg')
#
#     def __repr__(self):
#         return '<Addproduct %r>' % self.name
#
#
# class Brand(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False, unique=True)
#
#
# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False, unique=True)
