from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from config import BaseConfig

db = SQLAlchemy()

def CreateApp():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    db.init_app(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    from views import checkout, reserve, report, garage
    from models import Level, VehicleType, Reservation, ParkingSpot

    app.register_blueprint(garage)
    admin = Admin(app)
    admin.add_view(ModelView(VehicleType, db.session))
    admin.add_view(ModelView(Reservation, db.session))
    admin.add_view(ModelView(Level, db.session))
    admin.add_view(ModelView(ParkingSpot, db.session))
    return app
