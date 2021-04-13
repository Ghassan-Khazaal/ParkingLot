from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
from models_service import *

def __setUp():
    with app.test_request_context():
        db.create_all()

def __tearDown():
    with app.test_request_context():
        db.session.remove()
        db.drop_all()

def __addLevels(cnt):
    for i in range(cnt):
        level = Level()
        level.label = str(i+1)
        db.session.add(level)
    db.session.commit()
    

def __addVehicleTypes(cnt):
    for i in range(cnt):
        vt = VehicleType()
        vt.id = i+1
        vt.name = 'T%s' % (i+1)
        db.session.add(vt)
    db.session.commit()

def __addSpots(levelId, vehicleTypeId, cnt, lblPrefix):
    for i in range(cnt):
        spot = ParkingSpot()
        spot.vehicleTypeId = vehicleTypeId
        spot.label = "%s%s" % (lblPrefix, i)
        spot.levelId = levelId
        db.session.add(spot)
    db.session.commit()


def test_reserve():
    __setUp()
    try:
        with app.test_request_context():
            __addLevels(2)
            __addVehicleTypes(2)
            __addSpots(1, 1, 1, 'C')
            __addSpots(2, 1, 1, 'C')
            __addSpots(1, 2, 1, 'M')
            
            # reserve M
            result = reserve(1, 2)
            assert result['status'] == Constants.Status.Success
            assert result['data']['level'] == 1
            assert result['data']['label'] == 'M0'

            # reserve M, again
            result = reserve(1, 2)
            assert result['status'] == Constants.Status.Error
            assert result['data'] == Constants.Messages.Already_In

            # reserve M, No more space for M
            result = reserve(2, 2)
            assert result['status'] == Constants.Status.Error
            assert result['data'] == Constants.Messages.Full

            # reserve C, success
            result = reserve(2, 1)
            assert result['status'] == Constants.Status.Success
            assert result['data']['level'] == 1
            assert result['data']['label'] == 'C0'
            
            # reserve C, second level, success
            result = reserve(3, 1)
            assert result['status'] == Constants.Status.Success
            assert result['data']['level'] == 2
            assert result['data']['label'] == 'C0'
    finally:
        __tearDown()

def test_checkout():
    __setUp()
    try:
        with app.test_request_context():
            __addLevels(2)
            __addVehicleTypes(2)
            __addSpots(1, 1, 1, 'C')
            __addSpots(2, 1, 1, 'C')
            __addSpots(1, 2, 1, 'M')
            
            # checkout, success
            reserve(1, 2)
            result = checkout(1)
            assert result['status'] == Constants.Status.Success
            result = reserve(1, 2)
            assert result['status'] == Constants.Status.Success

            # checkout, id not in the garage
            result = checkout(2)
            assert result['status'] == Constants.Status.Error
            assert result['data'] == Constants.Messages.Not_In
    finally:
        __tearDown()

def test_status():
    __setUp()
    try:
        with app.test_request_context():
            __addLevels(2)
            __addVehicleTypes(2)
            __addSpots(1, 1, 2, 'C')
            __addSpots(2, 1, 2, 'C')
            __addSpots(1, 2, 5, 'M')
            
            reserve(1, 1)
            reserve(2, 1)
            reserve(3, 1)
            checkout(2)
            reserve(4, 2)
            reserve(5, 2)
            result = report()
            assert result['status'] == Constants.Status.Success
            expectedStatus = {
                    "1":{
                        "T1":{
                            "all":2,
                            "taken":1,
                            "free":1
                        },
                        "T2":{
                            "all":5,
                            "taken":2,
                            "free":3
                        }
                    },
                    "2":{
                        "T1":{
                            "all":2,
                            "taken":1,
                            "free":1
                        }
                    }
            }
            assert json.dumps(result['data']) == json.dumps(expectedStatus)
    finally:
        __tearDown()
