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

    def get(self):
        status = request.args.get('status')
        if status is not None:
            return jsonify(orders_schema.dump(self.model.query.filter_by(status=f"{status}").order_by(self.model.id.desc()).all()))
        return jsonify(orders_schema.dump(self.model.query.order_by(self.model.id.desc()).all()))
    
    #@jwt_required()
    @use_kwargs(OrderSerializer)
    def post(self, **kwargs):
        try:
            order = self.model(**kwargs)
            car = Car.query.get(order.car_id)
            order.car_brand = car.brand
            order.car_model = car.model
            db.session.add(order)
            db.session.commit()
            return '', 204
        except AssertionError as err:
            return jsonify(msg=str(err))


class OrderView(BaseView):
    def __init__(self):
        self.model = Order

    def get(self, id):
        return jsonify(order_schema.dump(self.model.query.get(id)))
    
    #@jwt_required()
    @use_kwargs(OrderUpdateSerializer)
    def put(self, id, **kwargs):
        try:
            order = self.model.query.get(id)
            order.update(**kwargs)
            return '', 204
        except AssertionError as err:
            return jsonify(msg=str(err))
    
    #@jwt_required()
    def delete(self, id):
        order = self.model.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return '', 204


class CommentsView(BaseView):
    def __init__(self):
        self.model = Comment

    def get(self, id=None):
        return jsonify(comments_schema.dump(self.model.query.order_by(self.model.id.desc()).all()))
    
    @use_kwargs(CommentSerializer)
    def post(self, **kwargs):
        try:
            comment = self.model(**kwargs)
            db.session.add(comment)
            db.session.commit()
            return jsonify(msg='Created')
        except AssertionError as err:
            return jsonify(msg=f"{str(err)}")


class CitiesView(BaseView):
    def __init__(self):
        self.model = City

    def get(self):
        return jsonify(cities_schema.dump(self.model.query.all()))
    
    #@jwt_required()
    @use_kwargs(CitySerializer)
    def post(self, **kwargs):
        try:
            city = self.model(**kwargs)
            db.session.add(city)
            db.session.commit()
            return '', 204
        except AssertionError as err:
            return jsonify(msg=str(err))


class CityView(BaseView):
    def __init__(self):
        self.model = City

    def get(self, id):
        return jsonify(city_schema.dump(self.model.query.get(id)))
    
    #@jwt_required()
    @use_kwargs(CitySerializer)
    def put(self, id, **kwargs):
        try:
            city = self.model.query.get(id)
            city.update(**kwargs)
            return '', 204
        except AssertionError as err:
            return jsonify(msg=str(err))
    
    #@jwt_required()
    def delete(self, id):
        city = self.model.query.get(id)
        db.session.delete(city)
        db.session.commit()
        return '', 204


OrderView.register(bp, docs, "/order/<int:id>", "orderview")
CommentsView.register(bp, docs, "/comment", "commentsview")
OrdersView.register(bp, docs, "/orders", "ordersview")
CityView.register(bp, docs, "/city/<int:id>", "cityview")
CitiesView.register(bp, docs, "/cities", "citiesview")



