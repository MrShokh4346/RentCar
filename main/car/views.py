from main.car import bp
from main.models import *
from main import jwt
from flask_jwt_extended import get_jwt_identity, jwt_required
from main.serializers import *
from flask import jsonify, request
from flask_apispec import use_kwargs, marshal_with
from flask.views import MethodView
from flask_apispec import MethodResource
from main import docs


class CategoryView(MethodView):
    def __init__(self, model):
        self.model = model

    def _get_item(self, id):
        return self.model.query.get(id)

    def get(self, id=None):
        if id is not None:
            return jsonify(category_schema.dump(self.model.query.get(id)))
        return jsonify(categories_schema.dump(self.model.query.all()))
    
    @jwt_required()
    @use_kwargs(CategorySerializer)
    def post(self, **kwargs):
        category = self.model(**kwargs)
        db.session.add(category)
        db.session.commit()
        return jsonify(msg="Created")
    
    @jwt_required()
    @use_kwargs(CategorySerializer)
    def put(self, id, **kwargs):
        category = self._get_item(id)
        category.update(**kwargs)
        return '', 204
    
    @jwt_required()
    def delete(self, id):
        category = self._get_item(id)
        db.session.delete(category)
        db.session.commit()
        return '', 204
    

class ImageView(MethodView):
    def __init__(self, model):
        self.model = model

    def _get_item(self, id):
        return self.model.query.get(id)

    def get(self, id=None):
        if id is not None:
            return jsonify(image_schema.dump(self.model.query.get(id)))
        return jsonify(images_schema.dump(self.model.query.all()))
    
    @jwt_required()
    @use_kwargs(ImageSerializer)
    def post(self, **kwargs):
        image = self.model(**kwargs)
        db.session.add(image)
        db.session.commit()
        return jsonify(msg="Created")
    
    @jwt_required()
    @use_kwargs(ImageSerializer)
    def put(self, id, **kwargs):
        image = self._get_item(id)
        image.update(**kwargs)
        return '', 204
    
    @jwt_required()
    def delete(self, id):
        image = self._get_item(id)
        db.session.delete(image)
        db.session.commit()
        return '', 204
    

class CarView(MethodView):
    def __init__(self, model):
        self.model = model

    def _get_item(self, id):
        return self.model.query.get(id)

    def get(self, id=None):
        if id is not None:
            return jsonify(car_schema.dump(self.model.query.get(id)))
        return jsonify(cars_schema.dump(self.model.query.all()))
    
    @jwt_required()
    @use_kwargs(CarSerializer)
    def post(self, **kwargs):
        car = self.model(**kwargs)
        db.session.add(car)
        db.session.commit()
        return jsonify(msg="Created")
    
    @jwt_required()
    @use_kwargs(CarSerializer)
    def put(self, id, **kwargs):
        car = self._get_item(id)
        car.update(**kwargs)
        return '', 204
    
    @jwt_required()
    def delete(self, id):
        car = self._get_item(id)
        db.session.delete(car)
        db.session.commit()
        return '', 204


bp.add_url_rule(f"/category/<int:id>", view_func=CategoryView.as_view('category-detail', Category))
docs.register(CategoryView, blueprint=bp.name)
bp.add_url_rule(f"/category/", view_func=CategoryView.as_view('category', Category))
docs.register(CategoryView, blueprint=bp.name)
bp.add_url_rule(f"/image/<int:id>", view_func=ImageView.as_view('image-detail', Image))
docs.register(ImageView, blueprint=bp.name)
bp.add_url_rule(f"/image/", view_func=ImageView.as_view('image', Image))
docs.register(ImageView, blueprint=bp.name)
bp.add_url_rule(f"/car/<int:id>", view_func=CarView.as_view('car-detail', Car))
docs.register(CarView, blueprint=bp.name)
bp.add_url_rule(f"/car/", view_func=CarView.as_view('car', Car))
docs.register(CarView, blueprint=bp.name)


