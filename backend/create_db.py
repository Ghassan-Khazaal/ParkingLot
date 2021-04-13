from app import db, CreateApp
from models import *

app = CreateApp()
with app.app_context():
    db.create_all()