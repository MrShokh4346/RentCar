from main.car import bp
from main.models import *
from main import jwt
from flask_jwt_extended import get_jwt_identity, jwt_required
from main.serializers import *
from flask import jsonify, request
from flask_apispec import use_kwargs, marshal_with
from main import docs
from main.base_view import BaseView


class CategoriesView(BaseView):
    def __init__(self):
        self.model = Category

    def get(self):
        return jsonify(categories_schema.dump(self.model.query.all()))
        
    #@jwt_required()
    @use_kwargs(CategorySerializer)
    def post(self, **kwargs):
        category = self.model(**kwargs)
        db.session.add(category)
        db.session.commit()
        return '', 204


class CategoryView(BaseView):
    def __init__(self):
        self.model = Category

    def get(self, id):
        return jsonify(category_schema.dump(self.model.query.get(id)))
    
    #@jwt_required()
    @use_kwargs(CategorySerializer)
    def put(self, id, **kwargs):
        category = self.model.query.get(id)
        category.update(**kwargs)
        return '', 204
    
    #@jwt_required()
    def delete(self, id):
        category = self.model.query.get(id)
        db.session.delete(category)
        db.session.commit()
        return '', 204


class CarImagesView(BaseView):
    def __init__(self):
        self.model = Image

    def get(self, car_id):
        return jsonify(images_schema.dump(self.model.query.filter_by(car_id=car_id).all()))


class ImagePostView(BaseView):
    def __init__(self):
        self.model = Image

    #@jwt_required()
    @use_kwargs(ImageSerializer)
    def post(self, **kwargs):
        image = self.model(**kwargs)
        db.session.add(image)
        db.session.commit()
        return '', 204


class ImageView(BaseView):
    def __init__(self):
        self.model = Image

    def _get_item(self, id):
        return self.model.query.get(id)

    def get(self, id=None):
        return jsonify(image_schema.dump(self.model.query.get(id)))

    #@jwt_required()
    @use_kwargs(ImageSerializer)
    def put(self, id, **kwargs):
        image = self._get_item(id)
        image.update(**kwargs)
        return '', 204
    
    #@jwt_required()
    def delete(self, id):
        image = self._get_item(id)
        db.session.delete(image)
        db.session.commit()
        return '', 204


class CarsByCategoryView(BaseView): 
    def __init__(self):
        self.model = Car

    def get(self, category_id):
        page = int(request.args.get('page', 1))
        cars = db.paginate(db.select(self.model).filter(self.model.category_id==category_id).order_by(self.model.id.desc()), page=page, per_page=8)
        data = cars_many_schema.dump(cars)
        count = 0
        for car in cars:
            image = Image.query.filter_by(car_id=car.id).first()
            data[count]['image'] =[{"body":image.body}] if image else []
            count += 1
        return jsonify(data)

class CarsView(BaseView): 
    def __init__(self):
        self.model = Car

    def get(self):
        page = int(request.args.get('page', 1))
        cars = db.paginate(db.select(self.model).order_by(self.model.id.desc()), page=page, per_page=8)
        data = cars_many_schema.dump(cars)
        count = 0
        for car in cars:
            image = Image.query.filter_by(car_id=car.id).first()
            data[count]['image'] =[{"body":image.body}] if image else []
            count += 1
        return jsonify(data)
    
    #@jwt_required()
    @use_kwargs(CarSerializer)
    def post(self, **kwargs):
        car = self.model(**kwargs)
        db.session.add(car)
        db.session.commit()
        return '', 204


class CarView(BaseView):
    def __init__(self):
        self.model = Car

    def _get_item(self, id):
        return self.model.query.get(id)

    def get(self, id=None):
        if id is not None:
            return jsonify(car_schema.dump(self.model.query.get(id)))
        return jsonify(cars_schema.dump(self.model.query.order_by(self.model.id.desc()).all()))
    
    #@jwt_required()
    @use_kwargs(CarSerializer)
    def put(self, id, **kwargs):
        car = self._get_item(id)
        car.update(**kwargs)
        return '', 204
    
    #@jwt_required()
    def delete(self, id):
        car = self._get_item(id)
        db.session.delete(car)
        db.session.commit()
        return '', 204


class SearchView(BaseView):
    def __init__(self):
        self.model = Car

    def get(self, name):
        return jsonify(cars_schema.dump(self.model.query.filter((self.model.model.like(f"%{name}%")) | (self.model.brand.like(f"%{name}%"))).order_by(self.model.id.desc()).all()))


CategoryView.register(bp, docs, "/category/<int:id>", "categoryview")
CategoriesView.register(bp, docs, "/categories", "categoriesview")
CarImagesView.register(bp, docs, "/images/<int:car_id>", "carimagesview")
ImageView.register(bp, docs, "/image/<int:id>", "imageview")
ImagePostView.register(bp, docs, "/image", "imagepostview")
CarsByCategoryView.register(bp, docs, "/cars/<int:category_id>", "carsbycategoryview")
CarView.register(bp, docs, "/car/<int:id>", "carview")
CarsView.register(bp, docs, "/cars", "carsview")
SearchView.register(bp, docs, "/search/<string:name>", "searchview")
