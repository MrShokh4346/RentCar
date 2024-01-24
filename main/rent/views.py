from main.rent import bp
from main.models import *
from main import jwt, docs
from flask_jwt_extended import get_jwt_identity, jwt_required
from main.serializers import *
from flask import jsonify, request
from flask_apispec import use_kwargs, marshal_with
from flask.views import MethodView
from flask_apispec.views import MethodResource
from main.base_view import BaseView


class OrdersView(BaseView):
    def __init__(self):
        self.model = Order

    def get(self, id=None):
        return jsonify(orders_schema.dump(self.model.query.order_by(self.model.id.desc()).all()))


class OrderView(BaseView):
    def __init__(self):
        self.model = Order

    def get(self, id):
        return jsonify(order_schema.dump(self.model.query.get(id)))
    
    @jwt_required()
    @use_kwargs(OrderSerializer)
    def post(self, **kwargs):
        order = self.model(**kwargs)
        car = Car.query.get(order.car_id)
        order.car_brand = car.brand
        order.car_model = car.model
        db.session.add(order)
        db.session.commit()
        return jsonify(msg="Created")
    
    @jwt_required()
    @use_kwargs(OrderSerializer)
    def put(self, id, **kwargs):
        order = self._get_item(id)
        order.update(**kwargs)
        return '', 204
    
    @jwt_required()
    def delete(self, id):
        order = self._get_item(id)
        db.session.delete(order)
        db.session.commit()
        return '', 204


OrderView.register(bp, docs, "/order/<int:id>", "orderview")
OrdersView.register(bp, docs, "/orders", "ordersview")


