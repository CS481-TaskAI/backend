#Connects with mysql container and creates tables

#SQLAlchemy
from server.models import *
from server import db, create_app
db.create_all(app=create_app())
    