from app import db
from models import *
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
import traceback

class Constants:

    class Messages:
        Already_In = 'The vehicle is already in the garage'
        Not_In = 'The vehicle is not in the garage'
        Full = 'The garage is full'
        Server_Error = 'Server error, please contact the support'
        Wrong_Vehicle_Type = 'Wrong vehicle type'

    class Status:
        Error = 'Error'
        Success = 'Success'

serverErrorResponse = {
    "status": Constants.Status.Error,
    "data": Constants.Messages.Server_Error
} 

# Helper Methods

def __getVehicleReservation(vehicleId):
    """
    Get vehicle current reservation if exists
    Args:
        vehicleId (str): vehicleId

    Returns:
        vehicleReservation: VehicleReservation instance if exist, else None
    """
    return db.session.query(Reservation).filter(and_(Reservation.vehicleId == vehicleId, Reservation.checkoutTimestamp == None)).first()

def __getAvailableSpot(vehicleType):
    """
    Get an available spot for a vehicle if exists
    Args:
        vehicleType (int): vehicleTypeId

    Returns:
        ParkingSpot: ParkingSpot instance if exists, else None
    """
    sq = db.session.query(Reservation.parkingSpotId).filter(Reservation.checkoutTimestamp == None).subquery()
    return db.session.query(ParkingSpot) \
              .filter(and_(ParkingSpot.vehicleTypeId == vehicleType, ParkingSpot.id.notin_(sq))) \
              .order_by(ParkingSpot.levelId) \
              .first()

def __getSpotsStatus():
    """
    Get spots' status, per level, per vehicleType
    Returns:
        Row: (levelId, vehicleType, totalNumberOfSpots, reservedSpots)
    """
    sq1 = db.session.query(ParkingSpot.levelId, ParkingSpot.vehicleTypeId, VehicleType.name, func.count(ParkingSpot.id).label('allSpots')) \
                    .join(VehicleType, ParkingSpot.vehicleTypeId == VehicleType.id) \
                    .group_by(ParkingSpot.levelId, ParkingSpot.vehicleTypeId, VehicleType.name) \
                    .subquery()

    sq2 = db.session.query(ParkingSpot.vehicleTypeId, ParkingSpot.levelId, func.count(Reservation.id).label('reservedSpots')) \
                    .join(ParkingSpot, Reservation.parkingSpotId == ParkingSpot.id) \
                    .filter(and_(Reservation.checkinTimestamp != None, Reservation.checkoutTimestamp == None)) \
                    .group_by(ParkingSpot.levelId, ParkingSpot.vehicleTypeId) \
                    .subquery()

    r = db.session.query(sq1.c.levelId, sq1.c.name, sq1.c.allSpots, func.coalesce(sq2.c.reservedSpots, 0)) \
                  .outerjoin(sq2, (sq1.c.levelId == sq2.c.levelId) & (sq1.c.vehicleTypeId == sq2.c.vehicleTypeId)).all()
    return r

def __getCurrentVehicles():
    """
    Get the vehicle ids for the ones that are currently in the garage
    Returns:
        list<str>: list of Ids
    """
    qs = db.session.query(Reservation.vehicleId).filter(Reservation.checkoutTimestamp == None).all()
    listIds = [v[0] for v in qs]
    return listIds

def __getVehicleTypes():
    """
    Get vehicle types
    Returns:
        list<dict>: list of dictionaries with ids and names
    """
    qs = db.session.query(VehicleType.id, VehicleType.name).all()
    listTypes = [{'id': vt[0], 'name': vt[1]} for vt in qs]
    return listTypes

#################################################################################################################################

def reserve(vehicleId, vehicleType):
    try:
        if (int(vehicleType) not in [vt['id'] for vt in __getVehicleTypes()]):
            result = {
                "status": Constants.Status.Error,
                "data": Constants.Messages.Wrong_Vehicle_Type 
            }
        elif __getVehicleReservation(vehicleId) is not None:
            result = {
                "status": Constants.Status.Error,
                "data": Constants.Messages.Already_In 
            }
        else:
            spot = __getAvailableSpot(vehicleType)
            if spot is None:
                result = {
                    "status": Constants.Status.Error,
                    "data": Constants.Messages.Full
                }
            else:
                reservation = Reservation()
                reservation.vehicleId = vehicleId
                reservation.parkingSpot = spot
                db.session.add(reservation)
                db.session.commit()
                result = {
                    "status": Constants.Status.Success,
                    "data": {
                        "level": spot.levelId,
                        "label": spot.label
                    }
                }
    except:
        traceback.print_exc()
        result = serverErrorResponse
    return result

def checkout(vehicleId):
    try:
        vehicle = __getVehicleReservation(vehicleId)
        if not vehicle:
            result = {
                "status": Constants.Status.Error,
                "data": Constants.Messages.Not_In 
            }
        else:
            vehicle.checkoutTimestamp = func.current_timestamp()
            db.session.commit()
            result = {
                "status": Constants.Status.Success,
                "data": "Done"
            }
    except:
        traceback.print_exc()
        result = serverErrorResponse
    return result

def report():
    try:
        qs = __getSpotsStatus()
        dictLevels = {}
        for q in qs:
            levelNumber = q[0]
            vehicleType = q[1]
            allSpots = q[2]
            reservedSpots = q[3]
            freeSpots = allSpots - reservedSpots
            if levelNumber not in dictLevels.keys():
                dictLevels[levelNumber] = {}
            dictLevels[levelNumber][vehicleType] = {
                "all": allSpots,
                "taken": reservedSpots,
                "free": freeSpots
            }
            result = {
                'status': Constants.Status.Success, 
                'data': dictLevels
            }
    except Exception as ex:
        traceback.print_exc()
        result = serverErrorResponse
    return result

def getCurrentVehicles():
    try:
        listIds = __getCurrentVehicles()
        result = {
            "status": Constants.Status.Success,
            "data": listIds
        }
    except:
        traceback.print_exc()
        result = serverErrorResponse
    return result

def getVehicleTypes():
    try:
        listTypes = __getVehicleTypes()
        result = {
            "status": Constants.Status.Success,
            "data": listTypes
        }
    except:
        traceback.print_exc()
        result = serverErrorResponse
    return result

# FOR TESTING ONLY
def initdb():
    Reservation.query.delete()
    ParkingSpot.query.delete()
    Level.query.delete()
    VehicleType.query.delete()
    db.session.commit()

    type1 = VehicleType()
    type1.name = 'Car'
    db.session.add(type1)

    type2 = VehicleType()
    type2.name = 'Motorbike'
    db.session.add(type2)

    l = Level()
    l.label = 1
    db.session.add(l)

    db.session.commit()
    lvlId = db.session.query(Level.id).one()[0]
    vt = db.session.query(VehicleType.id).all()[0][0]
    for i in range(3):
        spot = ParkingSpot()
        spot.vehicleTypeId = vt
        spot.label = str('C%s' % (i+1))
        spot.levelId = lvlId
        db.session.add(spot)

    vt = db.session.query(VehicleType.id).all()[1][0]

    for i in range(2):
        spot = ParkingSpot()
        spot.vehicleTypeId = vt
        spot.label = str('M%s' % (i+1))
        spot.levelId = lvlId
        db.session.add(spot)

    db.session.commit() 
    return "done"
