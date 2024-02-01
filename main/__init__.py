from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sqlalchemy import MetaData
from dotenv.main import load_dotenv
import os
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

load_dotenv()

naming_convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
docs = FlaskApiSpec()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost/rentcar"
    app.config["JWT_SECRET_KEY"] = os.environ['JWT_SECRET_KEY']
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["SECRET_KEY"] = os.environ['SECRET_KEY']

    app.config.update({
    'APISPEC_SPEC': APISpec(
        title='RentCar',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    })

    cors = CORS(app)

    db.init_app(app=app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    from main.car import bp as car_bp
    app.register_blueprint(car_bp, url_prefix="/car/v1")

    from main.rent import bp as rent_bp
    app.register_blueprint(rent_bp, url_prefix="/rent/v1")

    from main.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth/v1")

    docs.init_app(app)


    from main.models import Admin
    @app.cli.command('createadmin')
    def createadmin():  
        username = input("username: ")
        password = input("password: ")
        user = Admin(username=username, password=password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

    from main.models import City
    @app.cli.command('addcity')
    def addcity():  
        cities = ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Ajman', 'Ras Al Khaimah', 'Fujairah', 'Umm Al Quwain', 'Kalba', 'Madinat Zayed', 'Khor Fakkan', 'Dibba Al-Fujairah', 'Ruwais', 'Ghayathi', 'Dhaid', 'Jebel Ali', 'Liwa Oasis', 'Hatta', 'Ar-Rams', 'Dibba Al-Hisn', 'Al Jazirah Al Hamra', 'Abu al Abyad', 'Adhen', 'Al Ajban', 'Al Aryam', 'Al Awir', 'Al Badiyah', 'Al Bataeh', 'Al Bithnah', 'Al Faqa', 'Al Halah', 'Al Hamraniyah', 'Al Hamriyah', 'Al Jeer', 'Al Khawaneej', 'Al Lisaili', 'Al Madam', 'Al Manama', 'Al Mirfa', 'Al Qusaidat', 'Al Qor', 'Al Salamah', 'Al Shuwaib', 'Al Rafaah', 'Al Rashidya', 'Al Ruwayyah', 'Al Yahar', 'Asimah', 'Dalma', 'Dadna', 'Digdaga', 'Falaj Al Mualla', 'Ghalilah', 'Ghayl', 'Ghub', 'Habshan', 'Huwaylat', 'Khatt', 'Khor Khwair', 'Lahbab', 'Marawah', 'Masafi', 'Masfut', 'Mirbah', 'Mleiha', 'Nahil', 'Qidfa', "Sha'am", 'Sila', 'Sweihan', 'Wadi Shah', 'Zubarah']
        for city in cities:
            c = City(name=city)
            with app.app_context():
                db.session.add(c)
                db.session.commit()

    from main import models
    with app.app_context():
        db.create_all()

    return app