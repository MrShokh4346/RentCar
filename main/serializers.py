from marshmallow import Schema, validates, fields
from main.models import *


class AdminSerializer(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

admin_schema = AdminSerializer()


class ImageSerializer(Schema):
    id = fields.Integer(dump_only=True)
    body = fields.String(required=True)
    car_id = fields.Integer(required=True, load_only=True)

images_schema = ImageSerializer(many=True)
image_schema = ImageSerializer()


class CategorySerializer(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

categories_schema = CategorySerializer(many=True)
category_schema = CategorySerializer()


class CarSerializer(Schema):
    id = fields.Integer(dump_only=True)
    model = fields.String(required=True)
    brand = fields.String(required=True)
    doors = fields.Integer(required=True)
    image = fields.Nested(ImageSerializer, many=True, dump_only=True)
    fuel = fields.String(required=True)
    gear = fields.String(required=True)
    baggage = fields.Float(required=True)
    price_use = fields.Float(required=True)
    price_euro = fields.Float(required=True)
    price_arab = fields.Float(required=True)
    category_id = fields.Integer(required=True, load_only=True)
    category = fields.Nested(CategorySerializer, dump_only=True)

car_schema = CarSerializer()
cars_schema = CarSerializer(many=True)


class OrderSerializer(Schema):
    id = fields.Integer(dump_only=True)
    customer_name = fields.String(required=True)
    contact_number = fields.String(required=True)
    delivery = fields.Boolean(required=True)
    status = fields.Boolean(required=True)
    from_date = fields.DateTime(format='%Y-%m-%d')
    to_date = fields.DateTime(format='%Y-%m-%d')
    from_destination = fields.String(required=True)
    to_destination = fields.String(required=True)
    child_sit = fields.Boolean()
    car_brand = fields.String(required=True, dump_only=True)
    car_model = fields.String(required=True, dump_only=True)
    car = fields.Nested(CarSerializer, dump_only=True)
    car_id = fields.Integer(required=True, load_only=True)

order_schema = OrderSerializer()
orders_schema = OrderSerializer(many=True)


class OrderUpdateSerializer(Schema):
    id = fields.Integer(dump_only=True)
    customer_name = fields.String()
    contact_number = fields.String()
    delivery = fields.Boolean()
    status = fields.Boolean()
    from_date = fields.DateTime(format='%Y-%m-%d')
    to_date = fields.DateTime(format='%Y-%m-%d')
    from_destination = fields.String()
    to_destination = fields.String()
    child_sit = fields.Boolean()
    car_brand = fields.String(dump_only=True)
    car_model = fields.String(dump_only=True)
    car = fields.Nested(CarSerializer, dump_only=True)
    car_id = fields.Integer(load_only=True)

order_update_schema = OrderUpdateSerializer()




class CommentSerializer(Schema):
    id = fields.Integer(dump_only=True)
    author = fields.String(required=True)
    body = fields.String(required=True)

comment_schema = CommentSerializer()
comments_schema = CommentSerializer(many=True)


class CitySerializer(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

city_schema = CitySerializer()
cities_schema = CitySerializer(many=True)