from main.auth import bp
from main.models import *
from main.serializers import *
from flask import jsonify, request
from flask_apispec import use_kwargs, marshal_with
from flask.views import MethodView
from flask_apispec.views import MethodResource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token, get_jwt
from werkzeug.security import check_password_hash
from main import docs
from main.base_view import BaseView


class LoginView(BaseView):
    @use_kwargs(AdminSerializer)
    def post(self, **kwargs):
        user = Admin.query.filter_by(username=kwargs.get("username")).first()
        if user:
            if check_password_hash(user.password_hash, kwargs.get('password')):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return jsonify(access_token=access_token, refresh_token=refresh_token)
        return jsonify({"msg":"Incorrect password or username"})
    

class RefreshView(BaseView):
    @jwt_required(refresh=True)
    def post(self, **kwargs):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)
    
    
LoginView.register(bp, docs, "/login", "loginview")
RefreshView.register(bp, docs, "/refresh", "refreshview")
