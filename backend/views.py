from flask import jsonify, request
from models_service import *
from flask import Blueprint

garage = Blueprint('garage', __name__)

@garage.route("/reserve/", methods=["POST"])
def reserveSpot():
    vehicleId = request.form['vehicleId']
    vehicleType = request.form['vehicleType']
    result = reserve(vehicleId, vehicleType)
    return jsonify(result)

@garage.route("/checkout/", methods=["POST"])
def checkoutVehicle():
    vehicleId = request.form['vehicleId']
    result = checkout(vehicleId)
    return jsonify(result)

@garage.route("/status/", methods=["GET"])
def getStatus():
    result = report()
    return jsonify(result)

@garage.route("/current/", methods=["GET"])
def getCurrent():
    result = getCurrentVehicles()
    return jsonify(result)

@garage.route("/vtypes/", methods=["GET"])
def getVTypes():
    result = getVehicleTypes()
    return jsonify(result)

# FOR TESTING ONLY
@garage.route("/init/")
def initdp():
    result = initdb()
    return jsonify(result)
