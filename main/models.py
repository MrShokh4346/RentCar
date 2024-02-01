from main import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import validates 


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError("Passwprd was unrreadable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    car = db.relationship('Car', back_populates='category', lazy=True)

    def update(self, **kwargs):
        try:
            self.name = kwargs['name']
            db.session.commit()
        except:
            raise

    @validates('name')
    def validate_name(self, key, name):
        return name.lower()


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String)
    brand = db.Column(db.String)
    doors = db.Column(db.Integer)
    image = db.relationship('Image', back_populates='car', cascade="all,delete", lazy=True)
    fuel = db.Column(db.String)
    gear = db.Column(db.String)
    order = db.relationship('Order', back_populates='car', lazy=True)
    baggage = db.Column(db.Float)
    price_use = db.Column(db.Float)
    price_euro = db.Column(db.Float)
    price_arab = db.Column(db.Float)
    category = db.relationship('Category', back_populates='car', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="SET NULL"))

    def update(self, **kwargs):
        try:
            self.model = kwargs.get('model', self.model)
            self.brand = kwargs.get('brand', self.brand)
            self.doors = kwargs.get('doors', self.doors)
            self.fuel = kwargs.get('fuel', self.fuel)
            self.gear = kwargs.get('gear', self.gear)
            self.baggage = kwargs.get('baggage', self.baggage)
            self.price_use = kwargs.get('price_use', self.price_use)
            self.price_euro = kwargs.get('price_euro', self.price_euro)
            self.price_arab = kwargs.get('price_arab', self.price_arab)
            self.category_id = kwargs.get('category_id', self.category_id)
            db.session.commit()
        except:
            raise
    
    @validates('model')
    def validate_model(self, key, model):
        return model.lower()
    
    @validates('brand')
    def validate_brand(self, key, brand):
        return brand.lower()


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id", ondelete="CASCADE"))
    car = db.relationship('Car', back_populates='image',  lazy=True)

    def update(self, **kwargs):
        try:
            self.body = kwargs['body']
            db.session.commit()
        except:
            raise


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    contact_number = db.Column(db.String)
    delivery = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    from_date = db.Column(db.DateTime)
    to_date = db.Column(db.DateTime)
    from_destination = db.Column(db.String)
    to_destination = db.Column(db.String)
    car_brand = db.Column(db.String)
    car_model = db.Column(db.String)
    child_sit = db.Column(db.Boolean, default=False)
    car = db.relationship('Car', back_populates='order', lazy=True)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id", ondelete="SET NULL"))

    def update(self, **kwargs):
        try:
            if self.car_id != kwargs.get('car_id', self.car_id):
                car = Car.query.get(kwargs.get('car_id'))
                self.car_brand = car.brand
                self.car_model = car.model
            self.customer_name = kwargs.get('customer_name', self.customer_name)
            self.contact_number = kwargs.get('contact_number', self.contact_number)
            self.delivery = kwargs.get('delivery', self.delivery)
            self.status = kwargs.get('status', self.status)
            self.from_date = kwargs.get('from_date', self.from_date)
            self.to_date = kwargs.get('to_date', self.to_date)
            self.car_brand = kwargs.get('car_brand', self.car_brand)
            self.car_model = kwargs.get('car_model', self.car_model)
            self.car_id = kwargs.get('car_id', self.car_id)
            db.session.commit()
        except:
            raise


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    author = db.Column(db.String)

    @validates('author')
    def validate_brand(self, key, author):
        comment = Comment.query.filter_by(author=author.lower()).first()
        if comment:
            raise AssertionError("This email already exists")
        return author.lower()
    

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    @validates('name')
    def validate_brand(self, key, name):
        city = City.query.filter_by(name=name.lower()).first()
        if city:
            raise AssertionError("This city already exists")
        return name.lower()

    def update(self, **kwargs):
        try:
            self.name = kwargs.get('name', self.name)
            db.session.commit()
        except:
            raise