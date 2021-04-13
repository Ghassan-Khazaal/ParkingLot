from app import db
from sqlalchemy.sql import func

class VehicleType(db.Model):

    __tablename__ = 'VehicleType'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return self.name

class Level(db.Model):

    __tablename__ = 'Level'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    label = db.Column(db.String, unique=True)

    def __repr__(self):
        return '%s' % (self.label)

class ParkingSpot(db.Model):

    __tablename__ = 'ParkingSpot'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    label = db.Column(db.String)

    levelId = db.Column(db.Integer, db.ForeignKey('Level.id'), nullable=False)
    vehicleTypeId = db.Column(db.Integer, db.ForeignKey('VehicleType.id'), nullable=False)
    # width
    # length
    # barcode

    level = db.relationship('Level', foreign_keys=levelId)
    vehicleType = db.relationship('VehicleType', foreign_keys=vehicleTypeId)

    def __repr__(self):
        return 'L%s-%s' % (self.levelId, self.label)

class Reservation(db.Model):

    __tablename__ = 'Reservation'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vehicleId = db.Column(db.String, nullable=False)
    checkinTimestamp = db.Column(db.DateTime, nullable=False, default=func.current_timestamp())
    checkoutTimestamp = db.Column(db.DateTime, nullable=True)

    parkingSpotId = db.Column(db.ForeignKey('ParkingSpot.id'), nullable=False)

    parkingSpot = db.relationship('ParkingSpot', foreign_keys=parkingSpotId)
